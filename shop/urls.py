from django.urls import path
from .views import (
    ProductListView,
    CategoryListView,
)


app_name = 'shop'


urlpatterns = [
    path('', ProductListView.as_view(), name='home'),
    path('category/', CategoryListView.as_view(), name='category_list'),
]
