from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomePageView.as_view()),
    path('config/', views.StripeConfigView.as_view()),
    path('session/', views.StripeSessionView.as_view()),
    path('webhook/', views.StripeWebhookView.as_view()),
    path('account/', views.StripeAccountView.as_view()),
]