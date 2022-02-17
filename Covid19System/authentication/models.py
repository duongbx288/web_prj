from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    # MOH: Medical officer of health
    is_normal_user = models.BooleanField(default=True)
    is_MOH = models.BooleanField(default=False)