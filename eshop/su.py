import os
import random
import math

import django
import requests

from django.conf import settings
from faker import Faker

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eshop.settings")
# Call the django.setup() function before accessing Django settings.
django.setup()

from django.contrib.auth.models import User

from users.models import Profile

faker = Faker()


def create_admin():
    admin = User.objects.create(username="admin", email="lol@gmail.com")
    admin.is_staff = True
    admin.is_superuser = True
    admin.set_password("admin")
    admin.save()

    Profile.objects.create(user=admin)


create_admin()
