from .models import CustomUser
from .forms import (
    UserCreationForm,
    CustomUserForm,
)
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import AuthenticationForm
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import (
    View,
    CreateView,
    DetailView,
    UpdateView,
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
            if not user.is_deleted:
                user.is_logged_in = True
                user.save()

                login(request, user)
                request.session['success_message'] = 'Logged in successfully!'
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
