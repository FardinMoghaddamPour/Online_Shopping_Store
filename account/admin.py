from django.contrib import admin
from .models import CustomUser, Address


admin.site.register(CustomUser)
admin.site.register(Address)
