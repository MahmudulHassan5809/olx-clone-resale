from django.urls import path
from . import views

app_name = "pages"

urlpatterns = [
    path('how-it-works/', views.HowItWorks.as_view(), name='how_it_works'),
    path('faq/', views.Faq.as_view(), name='faq'),
    path('feedback/', views.FeedBack.as_view(), name='feedback'),
    path('contact/', views.Contact.as_view(), name='contact'),
    path('terms/', views.Terms.as_view(), name='terms'),
    path('terms/', views.Terms.as_view(), name='terms'),
    path('privacy/', views.Privacy.as_view(), name='privacy'),
]
