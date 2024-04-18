from django.db import models
from core.managers import LogicalManager


class TimeStampMixin(models.Model):
    """
    TimeStamp model mixin:

    fields:
        - create_at: DateTimeField (auto implement)
        - modify_at: DateTimeField (auto implement)
    """

    create_at = models.DateTimeField(auto_now_add=True, editable=False)
    modify_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True


class LogicalMixin(models.Model):
    """
    Logical model mixin:

    fields:
        - is_active: BooleanField (default True)
        - is_deleted: BooleanField (default False)
    """

    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    objects = LogicalManager()

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.save(update_fields=["is_deleted"])

    def deactivate(self):
        self.is_active = False
        self.save(update_fields=["is_active"])

    class Meta:
        abstract = True
