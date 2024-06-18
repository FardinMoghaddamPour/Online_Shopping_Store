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
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    is_logged_in = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    profile_image = models.ImageField(
        upload_to='profile_images/',
        blank=True,
        default='profile_images/User_Default_Profile_Pic.png'
    )

    # Custom manager

    objects = UserManager()

    # Override default fields

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'phone_number'
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


class Address(LogicalMixin, models.Model):

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='addresses')
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    address = models.TextField()
    zipcode = models.CharField(max_length=20)
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'

    def __str__(self):
        return f"{self.country}, {self.city} - {self.address}"

    def save(self, *args, **kwargs):
        if self.is_active:
            Address.objects.filter(user=self.user, is_active=True).exclude(id=self.id).update(is_active=False)
        super().save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        """
        Delete the instance.

        Args:
            using (str): Database alias. (Not actively used in this implementation)
            keep_parents (bool): If True, other related objects are not deleted.
                                 (Not actively used in this implementation)
        """
        if using:
            # ToDo: Perform delete operation using the specified database alias
            pass

        if keep_parents:
            # ToDo: Implement logic to keep related objects when deleting
            pass

        self.is_deleted = True
        self.is_active = False
        self.save(update_fields=['is_deleted', 'is_active'])

    def activate(self):
        if not self.is_active:
            Address.objects.filter(user=self.user, is_active=True).update(is_active=False)
            self.is_active = True
            self.save(update_fields=['is_active'])

    @classmethod
    def get_user_address(cls, pk, user):
        return cls.objects.filter(pk=pk, user=user, is_deleted=False).first()
