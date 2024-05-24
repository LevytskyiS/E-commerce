from django.db import models
from django_extensions.db.fields import AutoSlugField
from .utils import my_slugify_function


class NameSlugModel(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = AutoSlugField(
        populate_from="name", slugify_function=my_slugify_function, unique=True
    )

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class AttributesBase(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


# В Django, когда в классе Meta модели указано abstract = True,
# это означает, что данная модель является абстрактной.
# Абстрактная модель не создает таблицу в базе данных и
# не может быть непосредственно использована для создания объектов.
# Вместо этого она предназначена для наследования другими моделями,
# чтобы повторно использовать поля и методы,
# определенные в абстрактной модели.
