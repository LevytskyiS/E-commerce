from django.apps import apps
from rest_framework.serializers import ModelSerializer

from .serializers import (
    AttributeNameSerializer,
    AttributeValueSerializer,
    AttributeSerializer,
    BrandSerializer,
    ProductSerializer,
    NomenclatureSerializer,
    ImageSerializer,
    ShippingAddressSerializer,
)

PRODUCT_APP_NAME = "products"

model_serializers_mapping = {
    "AttributeName": AttributeNameSerializer,
    "AttributeValue": AttributeValueSerializer,
    "Attribute": AttributeSerializer,
    "Brand": BrandSerializer,
    "Product": ProductSerializer,
    "Nomenclature": NomenclatureSerializer,
    "Image": ImageSerializer,
    "ShippingAddress": ShippingAddressSerializer,
}


def get_app_models():
    return apps.get_app_config(PRODUCT_APP_NAME).get_models()


def get_serializer_model(key: str) -> ModelSerializer:
    """Find a proper serializer class based on the data provided to it."""
    return model_serializers_mapping.get(key, None)
