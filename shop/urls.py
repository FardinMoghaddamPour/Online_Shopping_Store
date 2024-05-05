from django.urls import path
from .views import (
    ProductListView,
    CategoryListView,
    ProductInCategoryListView
)


app_name = 'shop'


urlpatterns = [
    path('', ProductListView.as_view(), name='home'),
    path('category/', CategoryListView.as_view(), name='category_list'),
    path('category/<int:category_id>/products/', ProductInCategoryListView.as_view(), name='category_products'),
]
