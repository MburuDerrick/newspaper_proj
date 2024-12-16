from django.urls import path
from . import views

urlpatterns = [
    path("subscribe/", views.subscribe, name="subscribe"),
    path("validation/", views.mpesa_validation, name="mpesa_validation"),
    path("confirmation/", views.mpesa_confirmation, name="mpesa_confirmation"),
    ]
