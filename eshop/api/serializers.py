from rest_framework import serializers

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

    class Meta:
        model = AttributeName
        fields = ("id", "name")


class AttributeValueSerializer(serializers.ModelSerializer):

    class Meta:
        model = AttributeValue
        fields = ("id", "value")


class AttributeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attribute
        fields = ("id", "attribute_name", "attribute_value")


class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = ("id", "name")


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

    class Meta:
        model = ShippingAddress
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):

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
        fields = ("id", "order", "product", "quantity", "total_price")

    def get_total_price(self, obj: OrderItem):
        return obj.total_price()
