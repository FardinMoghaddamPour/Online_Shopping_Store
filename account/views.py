from .models import (
    CustomUser,
    Address,
)
from .forms import (
    UserCreationForm,
    CustomUserForm,
    CustomPasswordChangeForm,
    AddressForm,
)
from .serializers import AddressSerializer
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from utils.verification_code_generator import generate_verification_code
from django.views.generic import (
    View,
    CreateView,
    DetailView,
    UpdateView,
    TemplateView,
)
from rest_framework import viewsets, status
from rest_framework.authentication import (
    SessionAuthentication,
    TokenAuthentication,
)
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .tasks import send_verification_code_to_user
import json


class SignInView(View):
    template_name = 'signin.html'

    def get(self, request):
        form = AuthenticationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        local_cart = json.loads(request.POST.get('local_cart', '{}'))

        user = authenticate(request, phone_number=phone_number, password=password)
        if user is not None:
            if not user.is_deleted:
                user.is_logged_in = True
                user.save()

                login(request, user)
                request.session['success_message'] = 'Logged in successfully!'
                self.merge_carts(request, local_cart)
                request.session['logged_in'] = True
                return redirect(reverse_lazy('shop:home'))
            else:
                messages.error(request, 'Your account is disabled.')
        else:
            messages.error(request, 'Invalid phone number or password.')

        form = AuthenticationForm(request.POST)
        return render(request, self.template_name, {'form': form})

    @staticmethod
    def merge_carts(request, local_cart):
        session_cart = request.session.get('cart', {})

        for product_id, item in local_cart.items():
            if product_id in session_cart:
                session_cart[product_id]['quantity'] += item['quantity']
            else:
                session_cart[product_id] = item

        request.session['cart'] = session_cart
        request.session.modified = True


class CheckLoginStatusAPIView(APIView):
    @staticmethod
    def get(request):
        logged_in = request.session.pop('logged_in', False)
        return Response({'logged_in': logged_in})


class LogOutView(View):

    def post(self, request):
        cart_data = self.request.session.get('cart', {})

        self.request.user.is_logged_in = False
        self.request.user.save(update_fields=['is_logged_in'])

        logout(self.request)

        self.request.session['cart'] = cart_data
        self.request.session.modified = True

        return redirect('shop:home')


class UserCreateView(CreateView):

    model = CustomUser
    form_class = UserCreationForm
    template_name = 'signup.html'
    success_url = reverse_lazy('account:authenticate')


class UserProfileView(LoginRequiredMixin, DetailView):

    model = CustomUser
    template_name = 'user_profile.html'
    context_object_name = 'user'

    def get_object(self, queryset=None):

        user = self.request.user

        # noinspection PyUnresolvedReferences
        if user.is_authenticated and not user.is_deleted:
            return user
        raise Http404("You don't have permission to view this profile.")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        is_seller = self.request.user.groups.filter(name='Seller').exists()
        context['is_seller'] = is_seller
        return context


class EditProfileView(LoginRequiredMixin, UpdateView):

    model = CustomUser
    template_name = 'edit_profile.html'
    fields = ['first_name', 'last_name', 'age', 'profile_image']
    success_url = reverse_lazy('account:profile')

    def get_form_class(self):
        return CustomUserForm

    def get_object(self, queryset=None):
        return self.request.user


class AuthUserView(View):
    template_name = 'authenticate.html'
    success_url = '/success-authentication'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        if 'email' in request.POST:
            user_email = request.POST.get('email')
            verification_code = generate_verification_code()
            print(f"Sending task to send email to {user_email}")
            send_verification_code_to_user.apply_async(args=[user_email, verification_code])
            request.session['user_email'] = user_email
            request.session['verification_code'] = verification_code
            return render(request, self.template_name, {'show_verification_code_input': True})
        elif 'verification_code' in request.POST:
            verification_code = request.POST.get('verification_code')
            stored_code = request.session.get('verification_code')
            if verification_code == stored_code:
                user_email = request.session.get('user_email')
                try:
                    user = CustomUser.objects.get(email=user_email)
                    user.is_active = True
                    user.save()
                    messages.success(request, 'Account activated successfully!')
                except CustomUser.DoesNotExist:
                    messages.error(request, 'User with this email does not exist.')
                return HttpResponseRedirect(self.success_url)
            else:
                messages.error(request, 'Invalid verification code. Please try again.')
        return render(request, self.template_name)


class SuccessAuthenticationView(TemplateView):
    template_name = 'success_authentication.html'


class CustomPasswordChangeView(SuccessMessageMixin, PasswordChangeView):
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy('account:edit-profile')
    template_name = 'change_password.html'
    success_message = "Your password was successfully updated!"


class CreateAddressView(CreateView):
    model = Address
    form_class = AddressForm
    template_name = 'create_address.html'
    success_url = reverse_lazy('account:profile')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.is_active = False
        return super().form_valid(form)


class AddressViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = AddressSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return Address.objects.filter(user=self.request.user, is_deleted=False)

    @action(detail=True, methods=['post'])
    def delete_address(self, request, pk=None):
        address = Address.objects.filter(pk=pk, user=self.request.user, is_deleted=False).first()
        assert address is not None, 'Address not found'

        address.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
