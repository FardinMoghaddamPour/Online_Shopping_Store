from django.contrib import messages
from django.shortcuts import render
from django.views.generic import View
from .models import Product


class ProductListView(View):

    @staticmethod
    def get(request):

        if 'success_message' in request.session:
            messages.success(request, request.session.pop('success_message'))

        products = Product.objects.filter(is_active=True)
        return render(request, 'home.html', {'products': products})
