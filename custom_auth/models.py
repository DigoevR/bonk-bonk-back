from django.db import models
from django.contrib.auth.models import AbstractUser

from constants import DEFAULT_ELO

class User(AbstractUser):
    username = models.CharField(max_length=40, unique=True)
    first_name = models.CharField(max_length=40, null=False, blank=False)
    last_name = models.CharField(max_length=40, null=False, blank=False)
    paternal_name = models.CharField(max_length=40, null=False, blank=True, default='')
    elo = models.IntegerField(default=DEFAULT_ELO,)

