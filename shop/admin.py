from django.contrib import admin
from .models import (
    Category,
    Product,
    Inventory,
    WishlistProduct,
    Wishlist,
    Order,
    OrderItem,
    Discount,
    Coupon
)


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Inventory)
admin.site.register(WishlistProduct)
admin.site.register(Wishlist)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Discount)
admin.site.register(Coupon)
