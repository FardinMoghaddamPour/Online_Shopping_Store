from django.shortcuts import render
from django.views.generic import View
from .models import Product


class ProductListView(View):

    @staticmethod
    def get(request):
        products = Product.objects.filter(is_active=True)
        return render(request, 'home.html', {'products': products})
