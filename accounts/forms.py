from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    phone_number = forms.CharField()
    city = forms.CharField()

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone_number',
                  'city', 'password1', 'password2', )

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['phone_number'].required = True
        self.fields['city'].required = True


class LoginForm(forms.Form):
    username = forms.CharField(label='Your username', required=True)
    password = forms.CharField(widget=forms.PasswordInput())


class UpdateProfileForm(ModelForm):
    phone_number = forms.CharField()
    city = forms.CharField()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone_number', 'city',)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        user = self.request.user
        super(UpdateProfileForm, self).__init__(*args, **kwargs)

        self.fields['phone_number'].initial = user.user_profile.phone_number
        self.fields['first_name'].initial = user.first_name
        self.fields['last_name'].initial = user.last_name
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        # self.fields['bio'].initial = user.user_profile.bio
        self.fields['city'].initial = user.user_profile.city
