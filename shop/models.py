from account.models import CustomUser, Address
from core.models import LogicalMixin, TimeStampMixin
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from utils.coupon_generator import generate_coupon_code


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


class Discount(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='discount')
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        verbose_name = 'Discount'
        verbose_name_plural = 'Discounts'

    def __str__(self):
        return f"Discount for {self.product.name} - {self.discount_percentage}%"


class Order(models.Model):
    order_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return f'Order - {self.order_date}'


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'

    def __str__(self):
        return f'{self.product.name} - {self.quantity} units'

    def save(self, *args, **kwargs):

        if self.quantity > self.product.quantity:
            raise ValidationError(f"Insufficient quantity available for {self.product.name}.")

        self.price = self.product.price * self.quantity

        super().save(*args, **kwargs)


class Coupon(models.Model):
    coupon_code = models.CharField(
        max_length=8,
        unique=True,
        default=generate_coupon_code,
        help_text="Automatically generated alphanumeric coupon code"
    )
    amount_of_discount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(1), MaxValueValidator(1000000)],
        help_text="Amount of discount in dollars (between $1 and $1,000,000)"
    )
    is_active = models.BooleanField(default=True)
    rarity = models.CharField(
        max_length=20,
        choices=(
            ('Common', 'Common'),
            ('Uncommon', 'Uncommon'),
            ('Rare', 'Rare'),
            ('Epic', 'Epic'),
            ('Legendary', 'Legendary'),
        ),
        blank=True,
        null=True,
        editable=False,
        help_text="Rarity level based on amount of discount"
    )

    def __str__(self):
        return f"{self.coupon_code} - {self.amount_of_discount}"

    def save(self, *args, **kwargs):
        if 1 <= self.amount_of_discount <= 10:
            self.rarity = 'Common'
        elif 11 <= self.amount_of_discount <= 100:
            self.rarity = 'Uncommon'
        elif 101 <= self.amount_of_discount <= 1000:
            self.rarity = 'Rare'
        elif 1001 <= self.amount_of_discount <= 10000:
            self.rarity = 'Epic'
        elif 10001 <= self.amount_of_discount <= 1000000:
            self.rarity = 'Legendary'
        else:
            self.rarity = None

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Coupon'
        verbose_name_plural = 'Coupons'


class Cart(TimeStampMixin, LogicalMixin, models.Model):

    custom_user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='carts'
    )

    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name='cart'
    )

    address = models.OneToOneField(
        Address,
        on_delete=models.CASCADE,
        limit_choices_to={'is_active': True},
        related_name='cart'
    )
    coupon = models.OneToOneField(
        Coupon,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='cart')

    date_time = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    quantity = models.PositiveIntegerField(default=0)

    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    class Meta:
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'

    def __str__(self):
        return f'Cart - {self.date_time}'

    def save(self, *args, **kwargs):
        if not self.is_active:
            if self.order:
                self.order.is_active = False
                self.order.save(update_fields=['is_active'])

            if self.coupon:
                self.coupon.is_active = False
                self.coupon.save(update_fields=['is_active'])

            if self.order:
                order_items = self.order.order_items.all()
                for item in order_items:
                    product = item.product
                    if product.quantity >= item.quantity:
                        product.quantity -= item.quantity
                        product.save(update_fields=['quantity'])
                    else:
                        raise ValidationError(f"Insufficient quantity available for {product.name}.")

        super().save(*args, **kwargs)

    def calculate_total_price(self):
        """
        Calculate the total price of the cart based on order items and applied coupon (if any).
        """
        total_price = 0

        if self.order:
            order_items = self.order.order_items.all()
            for item in order_items:
                total_price += item.price

        if self.coupon and self.coupon.is_active:
            total_price -= self.coupon.amount_of_discount

        self.total_price = total_price
        self.save(update_fields=['total_price'])
