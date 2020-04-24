from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.utils.deconstruct import deconstructible


@deconstructible
class StringBaseValidator:
    message = _('Ensure all letters in this value is in english letters \
        (a:z and/or A:Z).')
    code = 'lower_uppercase'

    def __init__(self, value):
        cleaned = self.clean(value)
        params = {'code': self.code, 'show_value': cleaned, 'value': value}
        if self.check(cleaned):
            raise ValidationError(self.message, code=self.code, params=params)

    def check(self, value):
        value = value.lower()
        for i in value:
            if i < 'a' or i > 'z':
                return True

    def clean(self, x):
        return x


@deconstructible
class IsPhoneNumber(StringBaseValidator):
    message = _("Please Enter Valid phone number!")
    code = 'lowercase'

    def check(self, value):
        if not value.isnumeric():
            return True


@deconstructible
class PasswordValidation(StringBaseValidator):
    special_chars = "./!@#$%&;?"
    message = ['Please Enter valid password',
               '1) password length must be from 8 to 128 letters.',
               '2) password must contains lower case letters [a-z].',
               '3) password must contains upper case letters [A-Z].',
               '4) password must contains numbers. [0-9]',
               '5) password must contains special characters [. / ! @ # $ % & ; ?]'
               ]

    code = "valid_password"

    def check(self, value):
        r_1 = r_2 = r_3 = r_4 = r_5 = True
        if 8 <= len(value) <= 128:
            r_1 = False
        for char in value:
            if 'a' <= char <= 'z':
                r_2 = False
            elif 'A' <= char <= 'Z':
                r_3 = False
            elif '0' <= char <= '9':
                r_4 = False
            elif char in self.special_chars:
                r_5 = False
        return r_1 or r_2 or r_3 or r_4 or r_5
