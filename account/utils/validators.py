from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class UppercaseValidator:

    @staticmethod
    def validate(password, _user=None):
        """
        Validates that the password contains at least one uppercase letter.
        The '_user' parameter is included to match the expected signature of Django's
        password validation methods but is not used within this function.
        """
        if not any(char.isupper() for char in password):
            raise ValidationError(
                _("This password must contain at least one uppercase letter."),
                code='no_uppercase',
            )

    @staticmethod
    def get_help_text():
        return _("Your password must contain at least one uppercase letter.")
