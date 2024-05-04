from django.contrib import messages
from django.shortcuts import render
from django.views.generic import (
    View,
    ListView,
    DetailView,
)
from .models import Product, Category


class ProductListView(View):

    @staticmethod
    def get(request):

        if 'success_message' in request.session:
            messages.success(request, request.session.pop('success_message'))

        products = Product.objects.filter(is_active=True)
        return render(request, 'home.html', {'products': products})


class CategoryListView(ListView):
    model = Category
    template_name = 'category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return Category.objects.filter(parent_category__isnull=True)
