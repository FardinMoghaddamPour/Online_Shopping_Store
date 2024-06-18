from .models import (
    CustomUser,
    Address,
)
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field
from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class UserCreationForm(forms.ModelForm):

    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-input'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-input'}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = CustomUser
        fields = [
            'username',
            'password1',
            'password2',
            'phone_number',
            'email',
            'first_name',
            'last_name',
            'age',
            'profile_image'
        ]

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        user = self.instance
        try:
            password_validation.validate_password(password1, user)
        except ValidationError as e:
            self.add_error('password1', e)
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("The two password fields didn't match."))
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        password1 = self.cleaned_data.get('password1')
        if password1:
            user.set_password(password1)
        if commit:
            user.save()
        return user


class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'age', 'profile_image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('first_name', css_class='mt-2'),
            Field('last_name', css_class='mt-2'),
            Field('age', css_class='mt-2'),
            Field('profile_image', css_class='mt-2'),
        )


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Old Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'autofocus': True})
    )
    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label="Confirm New Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )

    def __init__(self, *args, **kwargs):
        super(CustomPasswordChangeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('old_password', css_class='mb-3'),
            Field('new_password1', css_class='mb-3'),
            Field('new_password2', css_class='mb-3'),
            Submit(
                'submit',
                'Change Password',
                css_class=(
                    'mt-4 bg-blue-500 hover:bg-blue-700 text-white font-bold '
                    'py-2 px-4 rounded'
                )
            )
        )

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("The two password fields didn't match.")
        password_validation.validate_password(password2, self.user)
        return password2


class BaseAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['country', 'city', 'address', 'zipcode']

    def __init__(self, *args, **kwargs):
        super(BaseAddressForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field(
                'country',
                css_class='shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight '
                          'focus:outline-none focus:shadow-outline'
            ),
            Field(
                'city',
                css_class='shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight '
                          'focus:outline-none focus:shadow-outline'
            ),
            Field(
                'address',
                css_class='shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight '
                          'focus:outline-none focus:shadow-outline'
            ),
            Field(
                'zipcode',
                css_class='shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight '
                          'focus:outline-none focus:shadow-outline'
            ),
        )


class AddressForm(BaseAddressForm):
    pass


class AddressUpdateForm(BaseAddressForm):
    pass
