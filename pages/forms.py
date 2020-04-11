from django.forms import ModelForm
from django import forms
from .models import FeedBack, Contact


class FeedBackForm(ModelForm):
    class Meta:
        model = FeedBack
        fields = ('__all__')
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'email': forms.TextInput(attrs={'placeholder': 'Email', 'type': 'email'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Phone Number'}),
            'message': forms.Textarea(
                attrs={'placeholder': 'Enter message here'}),
        }


class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = ('__all__')
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Who You Are'}),
            'email': forms.TextInput(attrs={'placeholder': 'example@email.com', 'type': 'email'}),
            'ad_url': forms.TextInput(attrs={'placeholder': 'Ad Url','type': 'url'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Phone Number'}),
            'message': forms.Textarea(
                attrs={'placeholder': 'Enter message here'}),
        }

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['phone_number'].label = "Phone"
