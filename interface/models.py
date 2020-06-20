from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=20, null=True)

    email = models.CharField(max_length=200, null=True)
    dateCreated = models.DateTimeField(auto_now_add=True, null=True)
    profilePicture = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name