from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django_extensions.db.fields import AutoSlugField

from products.utils import my_slugify_function


# Create your models here.
