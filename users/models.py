from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from helpers.validators import IsPhoneNumber


class User(AbstractUser):
    email = models.EmailField(
        _('Email'),
        max_length=150,
        unique=True,
        error_messages={
            'unique': _("A user with that email already exists."),
        },
    )
    phone_number = models.CharField(_('Phone Number'), blank=True, null=True, max_length=15, validators=[IsPhoneNumber])
    birth_date = models.DateField(_("Birth date"))

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
