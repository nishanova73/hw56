from django.db import models
from django.contrib.auth import get_user_model
from uuid import uuid4
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from datetime import timedelta


class Profile(models.Model):
    user: AbstractUser = models.OneToOneField(get_user_model(), related_name='profile',
                                              on_delete=models.CASCADE, verbose_name='User')
    birth_date = models.DateField(null=True, blank=True, verbose_name='Date of birth:')
    avatar = models.ImageField(null=True, blank=True, upload_to='user_pics', verbose_name='Avatar')

    def __str__(self):
        return self.user.get_full_name() + "'s Profile"

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'