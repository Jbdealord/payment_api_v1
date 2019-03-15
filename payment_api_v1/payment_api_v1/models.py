from django.db import models


class Account(models.Model):

    email = models.EmailField(null=False, blank=False)