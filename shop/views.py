from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import (
    View,
    ListView,
)
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import (
    Product,
    Category,
    Order,
)


class ProductListView(View):

    @staticmethod
    def get_cart_count(request):
        cart = request.session.get('cart', {})
        return sum(item['quantity'] for item in cart.values())

    @staticmethod
    def get(request):
        if 'success_message' in request.session:
            messages.success(request, request.session.pop('success_message'))

        products = Product.objects.filter(is_active=True).prefetch_related('discount')
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

    def post(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')
        product = get_object_or_404(Product, id=product_id)

        if hasattr(product, 'discount'):
            price = product.price * (1 - product.discount.discount_percentage / 100)
        else:
            price = product.price

        cart = self.request.session.get('cart', {})
        if product_id in cart:
            cart[product_id]['quantity'] += 1
        else:
            cart[product_id] = {'quantity': 1, 'price': str(price)}

        self.request.session['cart'] = cart
        self.request.session.modified = True
        return Response({'message': 'Product added to cart'}, status=status.HTTP_200_OK)


class CartView(View):
    @staticmethod
    def get(request):
        return render(request, 'cart.html')


class CartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart = self.request.session.get('cart', {})
        cart_items = []

        for product_id, item in cart.items():
            product = Product.objects.get(id=product_id)
            cart_items.append({
                'id': product.id,
                'name': product.name,
                'description': product.about,
                'price': item['price'],
                'quantity': item['quantity']
            })

        response_data = {
            'cart_items': cart_items,
            'cart_count': sum(item['quantity'] for item in cart_items),
            'total_price': sum(float(item['price']) * item['quantity'] for item in cart_items)
        }

        return Response(response_data)


class UpdateCartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = str(request.data.get('product_id'))
        quantity = request.data.get('quantity')
        product = get_object_or_404(Product, id=product_id)

        cart = self.request.session.get('cart', {})

        if quantity < 1:
            cart.pop(product_id, None)
        else:
            if product_id in cart:
                cart[product_id]['quantity'] = quantity
            else:
                cart[product_id] = {'quantity': quantity, 'price': str(product.price)}

        self.request.session['cart'] = cart
        self.request.session.modified = True

        return Response({'message': 'Cart updated successfully'})


class RemoveFromCartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = str(request.data.get('product_id'))

        cart = self.request.session.get('cart', {})
        cart.pop(product_id, None)

        self.request.session['cart'] = cart
        self.request.session.modified = True

        return Response({'message': 'Item removed from cart successfully'})


class CheckoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        cart = self.request.session.get('cart', {})

        if not cart:
            return Response({'message': 'Your cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            order = Order.objects.create(user=request.user)
            order.create_order_items(cart)
        except ValidationError as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        self.request.session['cart'] = {}
        self.request.session.modified = True

        return Response({'message': 'Order created successfully'}, status=status.HTTP_201_CREATED)
