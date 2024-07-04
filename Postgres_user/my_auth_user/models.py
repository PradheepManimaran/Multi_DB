from django.db import models

# Create your models here.

# myapp/models.py

from django.db import models

class User(models.Model):
    id = models.AutoField(primary_key=True)
    password = models.CharField(max_length=128)
    date_joined = models.DateTimeField()
    last_login = models.DateTimeField(null=True, blank=True)
    is_superuser = models.BooleanField(default=False)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
