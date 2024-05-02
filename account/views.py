from .models import CustomUser
from .forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import (
    View,
    CreateView
)


class SignInView(View):
    template_name = 'signin.html'

    def get(self, request):
        form = AuthenticationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')

        user = authenticate(request, phone_number=phone_number, password=password)
        if user is not None:
            if user.is_active:
                user.is_logged_in = True
                user.save()

                login(request, user)
                messages.success(request, 'Logged in successfully!')
                return redirect(reverse_lazy('shop:home'))
            else:
                messages.error(request, 'Your account is disabled.')
        else:
            messages.error(request, 'Invalid phone number or password.')

        form = AuthenticationForm(request.POST)
        return render(request, self.template_name, {'form': form})


class LogOutView(View):

    @staticmethod
    def post(request):
        request.user.is_logged_in = False
        request.user.save(update_fields=['is_logged_in'])
        logout(request)
        return redirect('shop:home')


class UserCreateView(CreateView):

    model = CustomUser
    form_class = UserCreationForm
    template_name = 'signup.html'
    success_url = reverse_lazy('account:signin')
