from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import (
    View,
    ListView,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Product, Category


class ProductListView(View):

    @staticmethod
    def get_cart_count(request):
        cart = request.session.get('cart', {})
        return sum(item['quantity'] for item in cart.values())

    @staticmethod
    def get(request):
        if 'success_message' in request.session:
            messages.success(request, request.session.pop('success_message'))

        products = Product.objects.filter(is_active=True)
        cart_count = ProductListView.get_cart_count(request)

        return render(request, 'home.html', {'products': products, 'cart_count': cart_count})


class CartCountView(View):
    @staticmethod
    def get(request):
        cart_count = ProductListView.get_cart_count(request)
        return JsonResponse({'cart_count': cart_count})


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


class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, *args, **kwargs):
        product_id = request.data.get('product_id')
        product = get_object_or_404(Product, id=product_id)

        cart = request.session.get('cart', {})
        if product_id in cart:
            cart[product_id]['quantity'] += 1
        else:
            cart[product_id] = {'quantity': 1, 'price': str(product.price)}

        request.session['cart'] = cart
        request.session.modified = True
        return Response({'message': 'Product added to cart'}, status=status.HTTP_200_OK)
