from django.contrib.auth.models import AbstractUser
from django.db import models


USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'
CHOICES = [
    ('admin', ADMIN),
    ('moderator', MODERATOR),
    ('user', USER)
]
MAX_LENGTH_EMAIL = 254
MAX_LENGTH_TEXT = 150
MAX_LENGTH_CONF_CODE = 30


class UserModel(AbstractUser):
    """Модель пользователя."""

    username = models.CharField(
        'Имя пользователя', max_length=MAX_LENGTH_TEXT,
        blank=False, unique=True
    )
    email = models.EmailField(
        'Email',
        max_length=MAX_LENGTH_EMAIL,
        blank=False,
        unique=True,
    )
    bio = models.TextField('О себе', blank=True)
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=MAX_LENGTH_CONF_CODE,
        blank=True, null=True
    )
    role = models.CharField(
        'Права юзера',
        max_length=MAX_LENGTH_TEXT, choices=CHOICES, default='user'
    )
    first_name = models.CharField(
        'Имя', max_length=MAX_LENGTH_TEXT, null=True, blank=True
    )
    last_name = models.CharField(
        'Фамилия', max_length=MAX_LENGTH_TEXT, null=True, blank=True
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-date_joined']

    def __str__(self):
        return self.username

    @property
    def is_user(self):
        return self.role == USER

    @property
    def is_admin(self):
        return self.role == ADMIN

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    def save(self, *args, **kwargs):
        if self.role == self.is_admin:
            self.is_staff = True
        super().save(*args, **kwargs)
