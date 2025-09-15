from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)
    PLAN_CHOICES = [
        ("free", "Free"),
        ("pro", "Pro"),
    ]
    plan = models.CharField(max_length=10, choices=PLAN_CHOICES, default="free")
