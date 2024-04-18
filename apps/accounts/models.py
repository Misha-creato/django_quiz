from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)

from django.db import models
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def create_user(self, email: str, password=str):
        if not email:
            raise ValueError('Требуется электронная почта')
        email = self.normalize_email(email)
        user = self.model(email=email, password=password)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email: str, password: str):
        email = self.normalize_email(email)
        user = self.model(email=email, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save()
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        unique=True,
        verbose_name='Адрес электронной почты'
    )
    is_superuser = models.BooleanField(
        default=False,
        verbose_name='Статус суперпользователя'
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name='Статус персонала'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активный'
    )
    email_confirmed = models.BooleanField(
        default=False,
        verbose_name='Адрес электронной почты подтвержден'
    )
    token = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name='Токен'
    )
    date_joined = models.DateTimeField(
        default=timezone.now,
        verbose_name='Дата регистрации'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
