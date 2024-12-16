from django.urls import path

from .views import SignUpView
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('signup/', SignUpView.as_view(), name = 'signup'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
   # path('subscribe/', SubscriptionView.as_view(), name='subscribe'),
    #path('subscription-details/', SubscriptionDetailsView.as_view(), name='subscription_details'),
    #path('subscribe/mpesa/', SubscribeMpesaView.as_view(), name='subscribe_mpesa'),
    #path('subscribe/stripe/', SubscribeStripeView.as_view(), name='stripe_checkout'),

]