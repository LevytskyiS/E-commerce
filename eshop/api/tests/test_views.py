import json

from django.test import TestCase
from django.forms.models import model_to_dict

from rest_framework.test import APIClient
from rest_framework import status
from products.models import AttributeName


class AttributeNameAPITest(TestCase):
    def setUp(self):
        AttributeName.objects.create(name="Color")
        self.client = APIClient()
        self.url = "/api/v1/attributename/"

    def perform_post(self, data):
        response = self.client.post(
            self.url, data=json.dumps(data), content_type="application/json"
        )
        return response

    def test_post(self):
        data = {"name": "Size"}
        response = self.perform_post(data)
        self.assertAlmostEqual(len(AttributeName.objects.all()), 2)
        self.assertTrue(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["name"], "Size")

    def test_object_exists_post(self):
        data = {"name": "Color"}
        response = self.perform_post(data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json()["name"], ["attribute name with this name already exists."]
        )
