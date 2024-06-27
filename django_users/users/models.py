import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Модель пользователя. В качестве id используется UUID4.
    В качестве уникального имени используется email.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(
        _("email address"),
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(
        _("active"),
        default=False,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=False,
        blank=True,
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "is_active"]

    def __str__(self):
        return self.email

    class Meta:
        ordering = ["date_joined"]
