from rest_framework import generics
from rest_framework import viewsets

from products.models import AttributeName, AttributeValue, Attribute, Brand, Product
from .serializers import (
    AttributeNameSerializer,
    AttributeValueSerializer,
    AttributeSerializer,
    BrandSerializer,
    ProductSerializer,
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


# Products
class ProductCreateAPIView(generics.CreateAPIView):
    serializer_class = ProductSerializer


class ProductGetUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
