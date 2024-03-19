from rest_framework import serializers

from products.models import AttributeName, AttributeValue, Attribute


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
        # depth = 1
