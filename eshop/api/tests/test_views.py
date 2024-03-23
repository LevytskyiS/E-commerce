import json
from datetime import datetime

from django.test import TestCase
from django.forms.models import model_to_dict
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status

from products.models import AttributeName
from orders.models import OrderItem, Order


class AttributeNameAPITest(TestCase):
    def setUp(self):
        AttributeName.objects.create(name="Color")
        self.client = APIClient()
        self.post_url = "/api/v1/attributename/"
        self.RUD_url = "/api/v1/attributename/<int:pk>/"
        self.get_list_url = "/api/v1/attributenames/"

    def perform_post(self, data):
        response = self.client.post(
            self.post_url, data=json.dumps(data), content_type="application/json"
        )
        return response

    def perform_read(self, id):
        url = f"/api/v1/attributename/{id}/"
        response = self.client.get(url, content_type="application/json")
        return response

    def perform_update(self, id, data):
        url = f"/api/v1/attributename/{id}/"
        response = self.client.patch(
            url, data=json.dumps(data), content_type="application/json"
        )
        return response

    def perform_delete(self, id):
        url = f"/api/v1/attributename/{id}/"
        response = self.client.delete(url, content_type="application/json")
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

    def test_get(self):
        new_obj = AttributeName.objects.create(name="Shade")
        response = self.perform_read(new_obj.id)
        obj, status_code = response.json(), response.status_code
        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertEqual(obj, model_to_dict(AttributeName.objects.get(id=new_obj.id)))

    def test_get_invalid_id(self):
        invalid_id = 9999
        response = self.perform_read(invalid_id)
        obj, status_code = response.json(), response.status_code
        self.assertAlmostEqual(status_code, status.HTTP_404_NOT_FOUND)

    def test_update(self):
        data = {"name": "Certificate"}
        new_obj = AttributeName.objects.create(name="Weight")
        response = self.perform_update(new_obj.id, data)
        obj, status_code = response.json(), response.status_code
        self.assertEqual(model_to_dict(AttributeName.objects.get(id=new_obj.id)), obj)
        self.assertAlmostEqual(status_code, status.HTTP_200_OK)

    def test_update_invalid_id(self):
        data = {"name": "Material"}
        response = self.perform_update(9999, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_invalid_data(self):
        obj = AttributeName.objects.get(name="Color")
        data = {"name": True}
        response = self.perform_update(obj.id, data)
        response_data, status_code = response.json(), response.status_code
        self.assertEqual(status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data["name"], ["Not a valid string."])

    def test_delete(self):
        new_obj = AttributeName.objects.create(name="Market")
        response = self.perform_delete(new_obj.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(AttributeName.objects.filter(name="Market")), 0)


class OrderAPITest(TestCase):
    def setUp(self) -> None:
        Order.objects.create(number="KT987654")
        self.client = APIClient()

    def perform_patch(self, data, id):
        url = f"/api/v1/order/{id}/"
        response = self.client.patch(
            url, data=json.dumps(data), content_type="application/json"
        )
        return response

    # def test_update(self):
    #     order = Order.objects.first()
    #     data = {"number": "123"}
    #     response = self.perform_patch(data, order.id)

    #     created_at = response.json()["created_at"]
    #     _updated_at = response.json()["updated_at"]
    #     obj_id = response.json()["id"]

    #     updated_at = datetime.strptime(_updated_at, "%Y-%m-%dT%H:%M:%S.%fZ")
    #     print(order.updated_at, updated_at)
    #     self.assertEqual(obj_id, order.id)
    #     self.assertNotEqual(updated_at, order.updated_at)


class OrderItemAPITest(TestCase):
    def setUp(self) -> None:
        AttributeName.objects.create(name="color")
        self.user = User.objects.create(username="admin", email="lol@gmail.com")
        self.user.set_password("admin")
        self.user.save()
        self.client = APIClient()

    def get_token(self):
        response = self.client.post(
            "/api/v1/token/",
            content_type="application/json",
            data=json.dumps({"username": self.user.username, "password": "admin"}),
        )
        return response.json()

    def test_get_otderitem_list(self):
        tokens = self.get_token()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
        url = "/api/v1/attributenames/"
        response = self.client.get(url, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
