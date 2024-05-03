from django.urls import path
from .views import (
    ProductListView,
    ReadCategoryView,
)


app_name = 'shop'


urlpatterns = [
    path('', ProductListView.as_view(), name='home'),
    path('category/', ReadCategoryView.as_view(), name='category_list'),
]
