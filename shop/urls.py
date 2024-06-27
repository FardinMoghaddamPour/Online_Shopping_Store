from django.urls import path
from .views import (
    ProductListView,
    CategoryListView,
    ProductInCategoryListView,
    AddToCartView,
    CartCountView,
    CartView,
    CartAPIView,
    UpdateCartAPIView,
    RemoveFromCartAPIView,
    CheckoutAPIView,
    OrderSummaryView,
    ActiveOrderAPIView
)


app_name = 'shop'


urlpatterns = [

    # CBV

    path('', ProductListView.as_view(), name='home'),
    path('category/', CategoryListView.as_view(), name='category_list'),
    path('category/<int:category_id>/products/', ProductInCategoryListView.as_view(), name='category_products'),
    path('cart/', CartView.as_view(), name='cart'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),

    # API view

    path('api/add-to-cart/', AddToCartView.as_view(), name='add-to-cart'),
    path('api/get-cart-count/', CartCountView.as_view(), name='get-cart-count'),
    path('api/cart/', CartAPIView.as_view(), name='cart-api'),
    path('api/update-cart/', UpdateCartAPIView.as_view(), name='update-cart'),
    path('api/remove-from-cart/', RemoveFromCartAPIView.as_view(), name='remove-from-cart'),
    path('api/checkout/', CheckoutAPIView.as_view(), name='checkout'),
    path('api/active-order/', ActiveOrderAPIView.as_view(), name='active-order'),
]
