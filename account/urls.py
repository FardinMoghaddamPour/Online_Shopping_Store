from django.urls import path
from .views import (
    SignInView,
    LogOutView,
)


app_name = 'account'


urlpatterns = [
    path('sign-in/', SignInView.as_view(), name='signin'),
    path('logout/', LogOutView.as_view(), name='logout'),
]
