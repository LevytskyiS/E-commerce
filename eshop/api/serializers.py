from collections import defaultdict

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.forms.models import model_to_dict
from django.db import transaction, IntegrityError

from products.models import (
    AttributeName,
    AttributeValue,
    Attribute,
    Brand,
    Product,
    Image,
    ProductImage,
)
from orders.models import Order, OrderItem, ShippingAddress, Nomenclature, Invoice


class AttributeNameSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    name = serializers.CharField()

    class Meta:
        model = AttributeName
        fields = ("id", "name")

    def create(self, validated_data):
        instance_id = validated_data.get("id")

        try:
            instance = AttributeName.objects.get(id=instance_id)
            if model_to_dict(instance) == validated_data:
                return instance
            instance.name = validated_data.get("name", instance.name)
            instance.save()
            return instance
        except AttributeName.DoesNotExist as e:
            return AttributeName.objects.create(**validated_data)


class AttributeValueSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    value = serializers.CharField()

    class Meta:
        model = AttributeValue
        fields = ("id", "value")

    def create(self, validated_data):
        instance_id = validated_data.get("id")

        try:
            instance = AttributeValue.objects.get(id=instance_id)
            if model_to_dict(instance) == validated_data:
                return instance
            instance.value = validated_data.get("value", instance.value)
            instance.save()
            return instance
        except AttributeValue.DoesNotExist as e:
            return AttributeValue.objects.create(**validated_data)


class AttributeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Attribute
        fields = ("id", "attribute_name", "attribute_value")

    def create(self, validated_data):
        instance_id = validated_data.get("id")

        try:
            instance = Attribute.objects.get(id=instance_id)
            if model_to_dict(instance) == validated_data:
                return instance
            instance.attribute_name = validated_data.get(
                "attribute_name", instance.attribute_name
            )
            instance.attribute_value = validated_data.get(
                "attribute_value", instance.attribute_value
            )
            instance.save()
            return instance
        except Attribute.DoesNotExist as e:
            return Attribute.objects.create(**validated_data)


class BrandSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    name = serializers.CharField()

    class Meta:
        model = Brand
        fields = ("id", "name", "subcategory", "category")

    def create(self, validated_data):
        instance_id = validated_data.get("id")

        try:
            instance = Brand.objects.get(id=instance_id)
            instance.name = validated_data.get("name", instance.name)
            instance.subcategory.set(
                validated_data.get("subcategory", instance.subcategory)
            )
            instance.category.set(validated_data.get("category", instance.category))
            instance.save()
            return instance
        except Brand.DoesNotExist as e:
            return Brand.objects.create(**validated_data)


class ProductSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    name = serializers.CharField()

    class Meta:
        model = Product
        fields = "__all__"

    def create(self, validated_data):
        instance_id = validated_data.get("id")

        try:
            instance = Product.objects.get(id=instance_id)
            instance.name = validated_data.get("name", instance.name)
            instance.brand = validated_data.get("brand", instance.brand)
            instance.sex = validated_data.get("sex", instance.sex)
            instance.brand = validated_data.get("brand", instance.brand)
            instance.category = validated_data.get("category", instance.category)
            instance.subcategory = validated_data.get(
                "subcategory", instance.subcategory
            )
            instance.attributes.set(
                validated_data.get("attributes", instance.attributes)
            )
            instance.save()
            return instance
        except Product.DoesNotExist as e:
            return Product.objects.create(**validated_data)


class NomenclatureSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    code = serializers.CharField()

    class Meta:
        model = Nomenclature
        fields = "__all__"

    def create(self, validated_data):
        instance_id = validated_data.get("id")

        try:
            instance = Nomenclature.objects.get(id=instance_id)
            instance.code = validated_data.get("code", instance.code)
            instance.product = validated_data.get("product", instance.product)
            instance.price = validated_data.get("price", instance.price)
            instance.quantity_available = validated_data.get(
                "quantity_available", instance.quantity_available
            )
            instance.save()
            return instance
        except Nomenclature.DoesNotExist as e:
            return Nomenclature.objects.create(**validated_data)


class ImageSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    image = serializers.URLField()

    class Meta:
        model = Image
        fields = "__all__"

    def create(self, validated_data):
        instance_id = validated_data.get("id")

        try:
            instance = Image.objects.get(id=instance_id)
            if model_to_dict(instance) == validated_data:
                return instance
            instance.name = validated_data.get("name", instance.name)
            instance.image = validated_data.get("image", instance.image)
            instance.save()
            return instance
        except Image.DoesNotExist as e:
            return Image.objects.create(**validated_data)


class ProductImageSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = ProductImage
        fields = "__all__"

    def create(self, validated_data):
        instance_id = validated_data.get("id")
        try:
            instance = ProductImage.objects.get(id=instance_id)
            if model_to_dict(instance) == validated_data:
                return instance
            instance.name = validated_data.pop("name", instance.name)
            instance.product = validated_data.get("product", instance.product)
            instance.image = validated_data.get("image", instance.image)
            instance.save()
            return instance
        except ProductImage.DoesNotExist as e:
            return ProductImage.objects.create(**validated_data)


class ShippingAddressSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = ShippingAddress
        fields = "__all__"


class OrderItemSerializer(serializers.ModelSerializer):

    total_price = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ("id", "order", "nomenclature", "quantity", "total_price")

    def get_total_price(self, obj: OrderItem):
        return obj.total_price()


class OrderSerializer(serializers.ModelSerializer):

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    total_price = serializers.SerializerMethodField()
    # order_item_ids = OrderItemSerializer(many=True)
    order_item_ids = serializers.SerializerMethodField()

    class Meta:
        # depth = 1
        model = Order
        fields = (
            "id",
            "code",
            "status",
            "user",
            "shipping_address",
            "created_at",
            "updated_at",
            "order_item_ids",
            "total_price",
        )

    def create(self, validated_data: dict):
        context = self.context
        request = context.get("request")
        items_data = request.data.get("order_item_ids")
        user = self.context["request"].user

        # Обработка данных для объединения дублирующихся номенклатур
        consolidated_items = defaultdict(int)

        if not items_data:
            raise ValidationError(
                {
                    "error": f"The nomenclatures to be ordered and their quantities are not provided"
                }
            )

        try:
            for item in items_data:
                consolidated_items[item["nomenclature"]] += item["quantity"]
        except KeyError:
            raise ValidationError(
                {"error": f"'nomenclature' or 'quantity' is missing. Chech the body"}
            )

        # Преобразование consolidated_items обратно в список словарей
        items_data = [
            {"nomenclature": k, "quantity": v} for k, v in consolidated_items.items()
        ]

        try:

            with transaction.atomic():
                order = Order.objects.create(**validated_data)

                for item in items_data:
                    try:
                        item_id = item.get("nomenclature")
                        nomenclature: Nomenclature = Nomenclature.objects.get(
                            id=item_id
                            # code=item.get("nomenclature")
                        )
                    except Nomenclature.DoesNotExist:
                        raise ValidationError(
                            {"error": f"Product with ID {item_id} does not exist"}
                        )

                    quantity = item["quantity"]
                    item["order"] = order
                    item["nomenclature"] = nomenclature

                    if quantity > nomenclature.quantity_available:
                        raise ValidationError(
                            {"error": f"Not enough stock for product ID {item_id}"}
                        )

                    nomenclature.quantity_available -= quantity
                    nomenclature.save()
                    order_item = OrderItem.objects.create(**item)

        except IntegrityError:
            raise ValidationError(
                {
                    "error": "An error occurred while processing your order. Please try again."
                }
            )

        return order

    def get_total_price(self, obj: Order):
        return obj.total_price()

    def get_order_item_ids(self, obj: Order):
        return [item.id for item in obj.items.all()]


class InvoiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Invoice
        fields = ("id", "order", "number")
