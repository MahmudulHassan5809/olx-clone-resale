from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from accounts.tokens import account_activation_token
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from products.models import Product, Category
from django.contrib.auth.models import User
from .forms import SignUpForm, LoginForm, UpdateProfileForm
from .mixins import AictiveUserRequiredMixin
from django.views import View, generic

# Create your views here.


class RegisterView(View):
    def get(self, request, *args, **kwrags):
        signup_form = SignUpForm()
        context = {
            'signup_form': signup_form,
            'title': 'Register'
        }
        return render(request, 'accounts/register.html', context)

    def post(self, request, *args, **kwrags):
        signup_form = SignUpForm(request.POST)
        if signup_form.is_valid():
            user = signup_form.save()
            user.refresh_from_db()
            user.user_profile.phone_number = signup_form.cleaned_data.get(
                'phone_number')
            user.user_profile.city = signup_form.cleaned_data.get('city')
            user.save()

            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            messages.success(
                request, ('Registration Completed.Please Confirm Your Email Address'))
            return redirect('accounts:login')
        else:
            context = {
                'signup_form': signup_form,
                'title': 'Register'
            }
            return render(request, 'accounts/register.html', context)


def activate(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.user_profile.email_confirmed = True
        user.user_profile.save()
        messages.success(
            request, ('Thank You For Confirm The Email.Your Account Will Be Activated Soon'))
        return redirect('accounts:login')
    else:
        messages.success(request, ('Activation link is invalid!'))
        return redirect('accounts:login')


class LoginView(View):
    def get(self, request, *args, **kwrags):
        login_form = LoginForm()
        context = {
            'login_form': login_form,
            'title': 'Login'
        }
        return render(request, 'accounts/login.html', context)

    def post(self, request, *args, **kwrags):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')

            user = authenticate(request, username=username,
                                password=password)
            if user is not None:
                if user.user_profile.email_confirmed and user.user_profile.active:
                    login(request, user)
                    return redirect('accounts:dashboard')
                else:
                    messages.error(request, ('Confirmed Your Email'))
                    return redirect('accounts:login')
            else:
                messages.error(
                    request, ('Invalid Credentials Or Account May Be Inactive'))
                return redirect('accounts:login')
        else:
            context = {
                'login_form': login_form,
                'title': 'Login'
            }
            return render(request, 'accounts/login.html', context)


class Dashboard(AictiveUserRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        updated_profile_form = UpdateProfileForm(request=request)
        context = {
            'title': 'Dashboard',
            'updated_profile_form': updated_profile_form
        }
        return render(request, 'accounts/dashboard.html', context)


class UpdateProfile(AictiveUserRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        city = request.POST.get('city')
        profile_image = request.FILES.get('image')

        if first_name:
            request.user.first_name = first_name
        if last_name:
            request.user.last_name = last_name
        if phone_number:
            request.user.user_profile.phone_number = phone_number
        if city:
            request.user.user_profile.city = city
        if profile_image:
            request.user.user_profile.profile_pic = profile_image

        request.user.save()
        request.user.user_profile.save()

        messages.success(request, "Profile Updated Successfully")
        return redirect('accounts:dashboard')


class ChangePassword(AictiveUserRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        chanage_password_form = PasswordChangeForm(user=request.user)
        context = {
            'title': 'Chnage Password',
            'chanage_password_form': chanage_password_form
        }
        return render(request, 'accounts/change_password.html', context)

    def post(self, request, *args, **kwargs):
        chanage_password_form = PasswordChangeForm(
            data=request.POST, user=request.user)
        context = {
            'title': 'Chnage Password',
            'chanage_password_form': chanage_password_form
        }
        if chanage_password_form.is_valid():
            chanage_password_form.save()
            update_session_auth_hash(request, chanage_password_form.user)
            messages.success(request, ('You have Changed Your Password...'))
            return redirect('accounts:change_password')
        else:
            return render(request, 'accounts/change_password.html', context)


class MyProduct(generic.ListView):
    model = Product
    context_object_name = 'my_ad_list'
    paginate_by = 10
    template_name = 'accounts/my_ad_list.html'

    def get_queryset(self):
        return self.request.user.user_products.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'{self.request.user.username}-Product'
        return context


class LogoutView(AictiveUserRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, ('You Have Been Logged Out..'))
        return redirect('accounts:login')
