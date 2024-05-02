from django.urls import path
from .views import (
    SignInView,
    LogOutView,
    UserCreateView,
    UserProfileView,
    EditProfileView,
    AuthUserView,
    SuccessAuthenticationView,
)


app_name = 'account'


urlpatterns = [
    path('sign-in/', SignInView.as_view(), name='signin'),
    path('logout/', LogOutView.as_view(), name='logout'),
    path('sign-up', UserCreateView.as_view(), name='sign-up'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('profile/edit/', EditProfileView.as_view(), name='edit-profile'),
    path('authenticate/', AuthUserView.as_view(), name='authenticate'),
    path('success-authentication/', SuccessAuthenticationView.as_view(), name='success-authentication'),
]
