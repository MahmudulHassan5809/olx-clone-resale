from django.shortcuts import render, redirect, get_object_or_404
from django.views import View, generic
from django.contrib import messages
from .models import Terms
from .forms import FeedBackForm, ContactForm
from accounts.mixins import AictiveUserRequiredMixin
# Create your views here.


class HowItWorks(View):
    def get(self, request, *args, **kwargs):
        context = {
            'title': 'How It Works',
        }

        return render(request, 'pages/how_it_works.html', context)


class Faq(View):
    def get(self, request, *args, **kwargs):
        context = {
            'title': 'Faq',
        }

        return render(request, 'pages/faq.html', context)


class FeedBack(View):
    def get(self, request, *args, **kwargs):
        feed_back_form = FeedBackForm()
        context = {
            'title': 'FeedBack',
            'feed_back_form': feed_back_form
        }

        return render(request, 'pages/feedback.html', context)

    def post(self, request, *args, **kwargs):
        feed_back_form = FeedBackForm(request.POST)

        if feed_back_form.is_valid():
            feed_back_form.save()
            messages.success(
                request, 'Thanks For Your Feedback.We Will Connect You Very Soon')
            return redirect('pages:feedback')
        else:
            context = {
                'title': 'FeedBack',
                'feed_back_form': feed_back_form
            }
            return render(request, 'pages/feedback.html', context)


class Contact(AictiveUserRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        contact_form = ContactForm()
        context = {
            'title': 'Contact Us',
            'contact_form': contact_form
        }

        return render(request, 'pages/contact.html', context)

    def post(self, request, *args, **kwargs):
        contact_form = ContactForm(request.POST)

        if contact_form.is_valid():
            contact_form.save()
            messages.success(
                request, 'Thanks For Your Feedback.We Will Connect You Very Soon')
            return redirect('pages:contact')
        else:
            context = {
                'title': 'Contact Us',
                'contact_form': contact_form
            }
            return render(request, 'pages/contact.html', context)


class Terms(generic.ListView):
    model = Terms
    context_object_name = 'all_terms'
    template_name = 'pages/terms.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Terms of Use'
        return context


class Privacy(View):
    def get(self,request,*args,**kwargs):
        context = {
            'title': 'Privacy Policy',
        }
        return render(request, 'pages/privacy.html', context)
