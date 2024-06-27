from account.models import Address
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import (
    View,
    ListView,
    TemplateView,
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
    OrderItem,
    Coupon,
    Cart,
)
from .serializers import OrderSerializer


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
            order = Order.objects.get(user=request.user, is_active=True)
        except Order.DoesNotExist:
            order = Order.objects.create(user=request.user)

        try:
            for product_id, item in cart.items():
                product = get_object_or_404(Product, id=product_id)

                if product.quantity < item['quantity']:
                    raise ValidationError(f'Not enough quantity for product {product.name}')

                order_item, created = OrderItem.objects.get_or_create(
                    order=order,
                    product=product,
                    defaults={'quantity': item['quantity'], 'price': product.price}
                )

                if not created:

                    order_item.quantity += item['quantity']
                    order_item.price = product.price * order_item.quantity
                    order_item.save()

                product.quantity -= item['quantity']
                product.save()

            order.total_price = sum(item.price for item in order.order_items.all())
            order.save()

        except ValidationError as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        self.request.session['cart'] = {}
        self.request.session.modified = True

        order_items = [{
            'name': item.product.name,
            'quantity': item.quantity,
            'price': item.price
        } for item in order.order_items.all()]

        return Response({
            'message': 'Order created successfully',
            'order_id': order.id,
            'order_items': order_items,
            'total_price': order.total_price
        }, status=status.HTTP_201_CREATED)


class OrderSummaryView(LoginRequiredMixin, TemplateView):
    template_name = 'order_summary.html'


class ActiveOrderAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            order = Order.objects.get(user=self.request.user, is_active=True)
            order_data = OrderSerializer(order).data
            return Response(order_data, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({'error': 'No active order found'}, status=status.HTTP_404_NOT_FOUND)


class CheckCouponAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        coupon_code = self.request.data.get('coupon')
        try:
            coupon = get_object_or_404(Coupon, coupon_code=coupon_code, is_active=True)
            return Response({'valid': True, 'discount': coupon.amount_of_discount}, status=200)
        except Coupon.DoesNotExist:
            return Response({'valid': False}, status=200)


class ConfirmOrderAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = self.request.user
        try:
            order = Order.objects.get(user=user, is_active=True)
        except Order.DoesNotExist:
            return Response({'message': 'No active order found'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            address = Address.objects.get(user=user, is_active=True)
        except Address.DoesNotExist:
            return Response(
                {
                    'message': 'You must have an active address to confirm the order.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        coupon_code = request.data.get('coupon_code')
        coupon = None
        if coupon_code:
            try:
                coupon = Coupon.objects.get(coupon_code=coupon_code, is_active=True)
            except Coupon.DoesNotExist:
                pass

        cart = Cart.objects.create(
            custom_user=user,
            order=order,
            address=address,
            coupon=coupon,
            is_active=True
        )
        cart.calculate_total_price()
        cart.deactivate_related_objects()

        cart.is_active = False
        cart.save(update_fields=['is_active'])

        return Response({'message': 'Order confirmed successfully', 'cart_id': cart.id}, status=status.HTTP_200_OK)
