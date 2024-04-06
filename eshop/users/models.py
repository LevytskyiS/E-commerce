from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)

    def get_absolute_url_client(self):
        return reverse("users:user_detail", kwargs={"slug": self.user.pk})
