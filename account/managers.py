from core.managers import LogicalManager
from django.contrib.auth.models import UserManager as BaseUserManager


class UserManager(LogicalManager, BaseUserManager):
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        extra_fields.setdefault("is_active", True)
        return self._create_user(username, email, password, **extra_fields)
