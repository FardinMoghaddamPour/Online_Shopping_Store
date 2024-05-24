from django.db import models


class LogicalQuerySet(models.QuerySet):
    def undelete(self):
        return super().update(is_deleted=False)

    def delete(self):
        return super().update(is_deleted=True)

    def activate(self):
        return super().update(is_active=True)

    def deactivate(self):
        return super().update(is_active=False)


class LogicalManager(models.Manager):

    def get_queryset_object(self):
        if not hasattr(self.__class__, "__queryset"):
            self.__class__.__queryset = LogicalQuerySet(self.model)

        return self.__queryset

    def get_queryset(self):
        return self.get_queryset_object().filter(is_deleted=False)

    @property
    def archived(self):
        return self.get_queryset_object()
