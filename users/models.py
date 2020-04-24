from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from helpers.validators import IsPhoneNumber, PasswordValidation
from helpers.numbers import gen_rand_number
from helpers.file_system import delete_file


class User(AbstractUser):
    image = models.ImageField(_("Profile image"), upload_to="images/profile", null=True, blank=True)
    email = models.EmailField(
        _('Email'),
        max_length=150,
        unique=True,
        error_messages={
            'unique': _("A user with that email already exists."),
        },
    )
    phone_number = models.CharField(_('Phone Number'), blank=True, null=True, max_length=15, validators=[IsPhoneNumber])
    birth_date = models.DateField(_("Birth date"), null=True, blank=True)
    password = models.CharField(_("password"), validators=[PasswordValidation], max_length=128,
                                help_text=_("1) password length is from 8 to 128 letters."
                                            "2) contains lower case letters."
                                            "3) contains upper case letters."
                                            "4) contains numbers."
                                            "5) contains special characters './!@#$%&;'"))
    email_verification_code = models.CharField(_("Email verification code"), max_length=6, null=True, blank=True)
    phone_number_verification_code = models.CharField(_("Phone number verification code"), max_length=6, null=True,
                                                      blank=True)
    email_verified = models.BooleanField(_("Email verified"), default=False)
    phone_number_verified = models.BooleanField(_("Phone number verified"), default=False)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self.__original_email = self.email
        self.__original_phone_number = self.phone_number
        self.__original_image = self.image

    def email_is_verified(self):
        return self.email_verified

    def phone_number_is_verified(self):
        return self.phone_number_verified

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        if self.email != self.__original_email:

            self.email_verified = False

        if self.phone_number != self.__original_phone_number:
            self.phone_number_verified = False

        if self.image != self.__original_image:
            if self.__original_image:
                delete_file([self.__original_image.path])

        super(User, self).save(force_insert, force_update, *args, **kwargs)
