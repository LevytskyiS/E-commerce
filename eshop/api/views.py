from rest_framework import generics
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import status
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.http import HttpRequest
from django.forms.models import model_to_dict

from products.models import (
    AttributeName,
    AttributeValue,
    Attribute,
    Brand,
    Product,
    Nomenclature,
    Image,
)
from orders.models import Order, OrderItem, ShippingAddress, Invoice
from .serializers import (
    AttributeNameSerializer,
    AttributeValueSerializer,
    AttributeSerializer,
    BrandSerializer,
    ProductSerializer,
    NomenclatureSerializer,
    ImageSerializer,
    OrderSerializer,
    OrderItemSerializer,
    ShippingAddressSerializer,
    InvoiceSerializer,
)
from .tasks import send_invoice

from .permissions import (
    IsOrderCreatorOrAdminUser,
    IsShippingAddressCreatorOrAdminUser,
    IsInvoiceUserOrAdminUser,
)
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
                    "saved_or_updated": saved_models,
                    "invalid": invalid_models,
                    "unknown": unknown_models,
                }
            },
            status=status.HTTP_200_OK,
        )


# AttributeName
class AttributeNameCreateAPIView(generics.CreateAPIView):
    serializer_class = AttributeNameSerializer
    permission_classes = [IsAdminUser]


class AttributeNameGetUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AttributeName.objects.all()
    serializer_class = AttributeNameSerializer
    permission_classes = [IsAdminUser]


class AttributeNameListAPIView(generics.ListAPIView):
    queryset = AttributeName.objects.all()
    serializer_class = AttributeNameSerializer
    permission_classes = [IsAuthenticated]


# AttributeValue
class AttributeValueCreateAPIView(generics.CreateAPIView):
    serializer_class = AttributeValueSerializer
    permission_classes = [IsAdminUser]


class AttributeValueGetUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AttributeValue.objects.all()
    serializer_class = AttributeValueSerializer
    permission_classes = [IsAdminUser]


class AttributeValueListAPIView(generics.ListAPIView):
    queryset = AttributeValue.objects.all()
    serializer_class = AttributeValueSerializer
    permission_classes = [IsAuthenticated]


# Attribute + ModelViewSet for RUD requests
class AttributeCreateAPIView(generics.CreateAPIView):
    serializer_class = AttributeSerializer
    permission_classes = [IsAdminUser]


class AttributeAPIViewSet(viewsets.ModelViewSet):
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer


# Brand
class BrandCreateAPIView(generics.CreateAPIView):
    serializer_class = BrandSerializer
    permission_classes = [IsAdminUser]


class BrandGetUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [IsAdminUser]


class BrandListAPIView(generics.ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [IsAuthenticated]


# Product
class ProductCreateAPIView(generics.CreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]


class ProductGetUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]


class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]


# Nomenclature
class NomenclatureCreateAPIView(generics.CreateAPIView):
    serializer_class = NomenclatureSerializer
    permission_classes = [IsAdminUser]


class NomenclatureGetUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Nomenclature.objects.all()
    serializer_class = NomenclatureSerializer
    permission_classes = [IsAdminUser]


class NomenclatureListAPIView(generics.ListAPIView):
    queryset = Nomenclature.objects.all()
    serializer_class = NomenclatureSerializer
    permission_classes = [IsAuthenticated]


# Image
class ImageCreateAPIView(generics.CreateAPIView):
    serializer_class = ImageSerializer
    permission_classes = [IsAdminUser]


class ImageGetUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [IsAdminUser]


class ImageListAPIView(generics.ListAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticated]


# ShippingAddress
class ShippingAddressCreateAPIView(generics.CreateAPIView):
    serializer_class = ShippingAddressSerializer
    permission_classes = [IsAuthenticated]


class ShippingAddressGetUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ShippingAddress.objects.all()
    serializer_class = ShippingAddressSerializer
    permission_classes = [IsShippingAddressCreatorOrAdminUser]


class ShippingAddressListAPIView(generics.ListAPIView):
    serializer_class = ShippingAddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ShippingAddress.objects.filter(user=self.request.user)


# Order
class OrderCreateAPIView(generics.CreateAPIView):
    # serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = OrderSerializer(data=request.data, context={"request": request})
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            # send_invoice.delay(serializer.data.get("id"))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderGetUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsOrderCreatorOrAdminUser]


class OrderListAPIView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by("created_at")


# OrderItem
class OrderItemCreateAPIView(generics.CreateAPIView):
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]


class OrderItemGetUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrderItem.objects.all().order_by("id")
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]


class OrderItemListAPIView(generics.ListAPIView):
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return OrderItem.objects.filter(order__user=self.request.user)


# Invoice
class InvoiceDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [IsInvoiceUserOrAdminUser]

    def get(self, request: HttpRequest, pk: int, format="json") -> Response:
        model = get_object_or_404(Invoice, id=pk)
        serialized_data = InvoiceSerializer(model).data
        return Response(serialized_data)
