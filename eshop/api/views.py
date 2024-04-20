from rest_framework import generics
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import status
from django.db import IntegrityError

from products.models import (
    AttributeName,
    AttributeValue,
    Attribute,
    Brand,
    Product,
    Nomenclature,
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
    NomenclatureSerializer,
    ImageSerializer,
    ProductImageSerializer,
    OrderSerializer,
    OrderItemSerializer,
    ShippingAddressSerializer,
)

from .permissions import IsOrderCreatorOrAdminUser
from .utils import get_app_models, get_serializer_model

app_models = [model.__name__ for model in get_app_models()]


# Import
class ImportAPIView(APIView):

    parser_classes = [JSONParser]

    def post(self, request, format="json") -> Response:
        saved_models, invalid_models, unknown_models = [], [], []
        json_data = request.data

        if not json_data:
            return Response({"result": "No data provided"}, status=200)

        for data in json_data:
            data_keys = data.keys()

            for key in data_keys:
                if key not in app_models:
                    unknown_models.append(data)
                    continue

                serializer_model = get_serializer_model(key)
                serializer = serializer_model(data=data[key])

                if not serializer.is_valid():
                    object_data = data[key]
                    object_data["error"] = serializer.errors
                    invalid_models.append(data)
                    continue

                try:
                    serializer.save()
                except IntegrityError as e:
                    object_data = data[key]
                    object_data["error"] = str(e)
                    invalid_models.append(data)
                    continue

                data[key] = serializer.data
                saved_models.append(data)

        return Response(
            {
                "data": {
                    "saved": saved_models,
                    "invalid": invalid_models,
                    "unknown": unknown_models,
                }
            },
            status=status.HTTP_200_OK,
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
    # For testing token
    # permission_classes = [IsAuthenticated]


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


# Nomenclature
class NomenclatureCreateAPIView(generics.CreateAPIView):
    serializer_class = NomenclatureSerializer


class NomenclatureGetUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Nomenclature.objects.all()
    serializer_class = NomenclatureSerializer


class NomenclatureListAPIView(generics.ListAPIView):
    queryset = Nomenclature.objects.all()
    serializer_class = NomenclatureSerializer


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
    permission_classes = [IsAuthenticated]


class ShippingAddressGetUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ShippingAddress.objects.all()
    serializer_class = ShippingAddressSerializer


class ShippingAddressListAPIView(generics.ListAPIView):
    queryset = ShippingAddress.objects.all().order_by("id")
    serializer_class = ShippingAddressSerializer


# Order
class OrderCreateAPIView(generics.CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAdminUser]


class OrderGetUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsOrderCreatorOrAdminUser]


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
