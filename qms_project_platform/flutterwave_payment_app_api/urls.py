from django.urls import path
from flutterwave_payment_app_api import views


urlpatterns = [
    path('api/wallet_top_up/', views.wallet_top_up, name='wallet_top_up'), 
    path('api/wallet_withdrawal/', views.wallet_withdrawal, name='wallet_witdrawal'),
    path('api/payment_success_redirect/', views.payment_success_redirect, name='payment_success_redirect_view'),
]