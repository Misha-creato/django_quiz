from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)

from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email: str, password: str, **extra_fields):
        if not email:
            raise ValueError('Требуется электронная почта')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email: str, password: str):
        return self.create_user(
            email=email,
            password=password,
            is_staff=True,
            is_superuser=True,
        )


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        unique=True,
        verbose_name='Адрес электронной почты',
    )
    is_superuser = models.BooleanField(
        default=False,
        verbose_name='Статус суперпользователя',
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name='Статус персонала',
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активный',
    )
    email_confirmed = models.BooleanField(
        default=False,
        verbose_name='Адрес электронной почты подтвержден',
    )
    url_hash = models.CharField(
        max_length=128,
        null=True,
        blank=True,
        verbose_name='Хэш',
    )
    date_joined = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата регистрации',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        db_table = 'users'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
