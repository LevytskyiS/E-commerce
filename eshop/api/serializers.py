from rest_framework import serializers
from django.forms.models import model_to_dict

from products.models import (
    AttributeName,
    AttributeValue,
    Attribute,
    Brand,
    Product,
    Image,
    ProductImage,
)
from orders.models import Order, OrderItem, ShippingAddress, Nomenclature


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

    class Meta:
        model = Brand
        fields = ("id", "name", "subcategory", "category")

    def create(self, validated_data):
        instance_id = validated_data.get("id")

        try:
            instance = Brand.objects.get(id=instance_id)
            if model_to_dict(instance) == validated_data:
                return instance
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

    class Meta:
        model = Product
        fields = "__all__"


class NomenclatureSerializer(serializers.ModelSerializer):

    class Meta:
        model = Nomenclature
        fields = "__all__"


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = "__all__"


class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = "__all__"


class ShippingAddressSerializer(serializers.ModelSerializer):

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = ShippingAddress
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    total_price = serializers.SerializerMethodField()
    order_item_ids = serializers.SerializerMethodField()

    class Meta:
        # depth = 1
        model = Order
        fields = (
            "id",
            "code",
            "user",
            "shipping_address",
            "created_at",
            "updated_at",
            "order_item_ids",
            "total_price",
        )

    def get_total_price(self, obj: Order):
        return obj.total_price()

    def get_order_item_ids(self, obj: Order):
        return [item.id for item in obj.items.all()]


class OrderItemSerializer(serializers.ModelSerializer):

    total_price = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ("id", "order", "nomenclature", "quantity", "total_price")

    def get_total_price(self, obj: OrderItem):
        return obj.total_price()
