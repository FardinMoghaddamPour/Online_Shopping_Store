from account.models import CustomUser
from core.models import LogicalMixin, TimeStampMixin
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    parent_category = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories'
    )

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Inventory(models.Model):
    name = models.CharField(max_length=255)
    capacity = models.PositiveIntegerField()

    class Meta:
        verbose_name = 'Inventory'
        verbose_name_plural = 'Inventories'

    def __str__(self):
        return self.name

    def clean(self):
        # Check if the capacity is valid (greater than zero)
        if self.capacity <= 0:
            raise ValidationError(_('Capacity must be a positive integer.'))

    def save(self, *args, **kwargs):
        # Ensure that the inventory's capacity is not exceeded
        if self.product:
            current_count = self.product.inventory_set.count()
            if current_count >= self.capacity:
                raise ValidationError(_('Inventory capacity exceeded for this product.'))
        super().save(*args, **kwargs)

    def can_accept_product(self):
        """
        Check if the inventory can accept a new product.

        Returns:
            bool: True if the inventory can accept a new product, False otherwise.
        """
        if self.product:
            current_count = self.product.inventory_set.count()
            return current_count < self.capacity
        return False


class Product(TimeStampMixin, LogicalMixin, models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='products')
    inventory = models.ForeignKey(
        'Inventory', on_delete=models.CASCADE, related_name='product', null=True, blank=True
    )
    name = models.CharField(max_length=255)
    about = models.TextField()
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.name

    def delete(self, using=None, keep_parents=False):
        """
        Override the delete method to set is_active to False before deletion.
        """
        self.is_active = False
        self.save(update_fields=['is_active'])
        super().delete(using=using, keep_parents=keep_parents)
