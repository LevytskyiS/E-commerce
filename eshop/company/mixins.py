from django.db import models


class MixinsModel(models.Model):
    name = models.CharField(max_length=30, unique=True, null=False)

    def __str__(self):
        return self.name
