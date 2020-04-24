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
