from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    is_verified = models.BooleanField(default=False)
    verify_code = models.CharField(max_length=32)
    age = models.IntegerField(default=0)  # Доп информация о пользаке
