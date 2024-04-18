from core.models import TimeStampMixin, LogicalMixin
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group, Permission
from django.core.validators import RegexValidator
from django.db import models
from account.managers import UserManager


class CustomUser(AbstractBaseUser, PermissionsMixin, TimeStampMixin, LogicalMixin):

    # RegEx validators

    username_validator = RegexValidator(
        regex=r"^[a-zA-Z0-9_]*$",
        message="Only alphanumeric characters and underscores are allowed."
    )
    phone_number_validator = RegexValidator(
        regex=r"^(?:\+989|09|00989)(?:0[0-5]|1[0-9]|2[0-3]|3[02-9]|9[0-46])[0-9]{7}$",
        message="Enter a valid Iranian phone number."
    )
    password_validator = RegexValidator(
        regex=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$",
        message="Password must contain at least 8 characters, including uppercase, lowercase, and digits."
    )

    # Fields
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    username = models.CharField(max_length=255, unique=True, validators=[username_validator])
    password = models.CharField(max_length=255, validators=[password_validator])
    phone_number = models.CharField(max_length=17, unique=True, validators=[phone_number_validator])
    email = models.EmailField(blank=True, null=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    is_logged_in = models.BooleanField(default=False)
    profile_image = models.ImageField(
        upload_to='profile_images/',
        blank=True,
        default='profile_images/User_Default_Profile_Pic.png'
    )

    # Custom manager

    objects = UserManager()

    # Override default fields

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:

        verbose_name = 'User'
        verbose_name_plural = 'Users'

        indexes = [
            models.Index(fields=["username"]),
            models.Index(fields=["email"]),
            models.Index(fields=["phone_number"]),
        ]

    def __str__(self):
        return self.username


groups = models.ManyToManyField(
    Group,
    verbose_name='groups',
    blank=True,
    related_name="custom_user_groups",
    help_text='The groups this user belongs to. A user will get all permissions granted '
              'to each of their groups.'
)

user_permissions = models.ManyToManyField(
    Permission,
    verbose_name='user permissions',
    blank=True,
    related_name="custom_user_permissions",
    help_text='Specific permissions for this user.'
)
