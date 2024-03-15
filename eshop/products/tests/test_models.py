from django.test import TestCase

from products.models import AttributeName


class AttributeNameTestCase(TestCase):
    def setUp(self):
        AttributeName.objects.create(name="Weight")

    def test_create_attribute_name(self):
        attr_name = AttributeName.objects.create(name="Color")
        self.assertEqual(len(AttributeName.objects.all()), 2)
        self.assertEqual(attr_name.name, "Color")

    def test_edit_attribute_name(self):
        attr_name = AttributeName.objects.get(name="Weight")
        attr_name.name = "Size"
        attr_name.save()
        self.assertEqual(attr_name.name, "Size")

    def test_delete_attribute_name(self):
        attr_name = AttributeName.objects.get(name="Weight")
        attr_name.delete()
        self.assertEqual(len(AttributeName.objects.all()), 0)
