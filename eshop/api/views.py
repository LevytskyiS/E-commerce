from rest_framework import generics

from products.models import AttributeName, AttributeValue
from .serializers import AttributeNameSerializer, AttributeValueSerializer


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
