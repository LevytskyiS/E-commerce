from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny

from products.models import (
    AttributeName,
    AttributeValue,
    Attribute,
    Brand,
    Product,
    Image,
    ProductImage,
)
from orders.models import Order, OrderItem, ShippingAddress
from .serializers import (
    AttributeNameSerializer,
    AttributeValueSerializer,
    AttributeSerializer,
    BrandSerializer,
    ProductSerializer,
    ImageSerializer,
    ProductImageSerializer,
    OrderSerializer,
    OrderItemSerializer,
    ShippingAddressSerializer,
)


# AttributeName
class AttributeNameCreateAPIView(generics.CreateAPIView):
    serializer_class = AttributeNameSerializer


class AttributeNameGetUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AttributeName.objects.all()
    serializer_class = AttributeNameSerializer


class AttributeNameListAPIView(generics.ListAPIView):
    queryset = AttributeName.objects.all()
    serializer_class = AttributeNameSerializer
    # For testing
    permission_classes = [IsAuthenticated]


# AttributeValue
class AttributeValueCreateAPIView(generics.CreateAPIView):
    serializer_class = AttributeValueSerializer


class AttributeValueGetUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AttributeValue.objects.all()
    serializer_class = AttributeValueSerializer


class AttributeValueListAPIView(generics.ListAPIView):
    queryset = AttributeValue.objects.all()
    serializer_class = AttributeValueSerializer


# Attribute + ModelViewSet for RUD requests
class AttributeCreateAPIView(generics.CreateAPIView):
    serializer_class = AttributeSerializer


class AttributeAPIViewSet(viewsets.ModelViewSet):
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer


# Brand
class BrandCreateAPIView(generics.CreateAPIView):
    serializer_class = BrandSerializer


class BrandGetUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class BrandListAPIView(generics.ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


# Product
class ProductCreateAPIView(generics.CreateAPIView):
    serializer_class = ProductSerializer


class ProductGetUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


# Image
class ImageCreateAPIView(generics.CreateAPIView):
    serializer_class = ImageSerializer


class ImageGetUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


class ImageListAPIView(generics.ListAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


# ProductImage
class ProductImageCreateAPIView(generics.CreateAPIView):
    serializer_class = ProductImageSerializer


class ProductImageGetUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer


class ProductImageListAPIView(generics.ListAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer


# ShippingAddress
class ShippingAddressCreateAPIView(generics.CreateAPIView):
    serializer_class = ShippingAddressSerializer


class ShippingAddressGetUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ShippingAddress.objects.all()
    serializer_class = ShippingAddressSerializer


class ShippingAddressListAPIView(generics.ListAPIView):
    queryset = ShippingAddress.objects.all().order_by("id")
    serializer_class = ShippingAddressSerializer


# Order
class OrderCreateAPIView(generics.CreateAPIView):
    serializer_class = OrderSerializer


class OrderGetUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.all().order_by("id")
    serializer_class = OrderSerializer


# OrderItem
class OrderItemCreateAPIView(generics.CreateAPIView):
    serializer_class = OrderItemSerializer


class OrderItemGetUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrderItem.objects.all().order_by("id")
    serializer_class = OrderItemSerializer


class OrderItemListAPIView(generics.ListAPIView):
    queryset = OrderItem.objects.all().order_by("id")
    serializer_class = OrderItemSerializer
