from django.contrib import messages
from django.shortcuts import render
from django.views.generic import (
    View,
    ListView,
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


class ProductInCategoryListView(ListView):

    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'

    def get_queryset(self):

        category_id = self.kwargs['category_id']
        category = Category.objects.get(id=category_id)
        descendant_categories = category.get_descendants(include_self=True)
        return Product.objects.filter(category__in=descendant_categories).distinct()
