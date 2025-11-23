from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from users.managers import UserManager


class User(AbstractUser):
    username = None
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=12, validators=[RegexValidator(r'^\+7\d{10}$')], blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    registration_date = models.DateField(auto_now_add=True)

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    objects = UserManager()

    class Meta:
        db_table = 'readers'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
