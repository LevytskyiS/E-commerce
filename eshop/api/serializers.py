from rest_framework import serializers

from products.models import AttributeName, AttributeValue, Attribute, Brand


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
