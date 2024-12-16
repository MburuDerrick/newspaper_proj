#from django.shortcuts import render
from django.shortcuts import render, redirect
#from django.utils.timezone import now, timedelta
#from django.http import HttpResponseForbidden
#from django.views.generic import FormView
from .models import Subscription
#from .forms import SubscriptionForm

from django.views.generic import CreateView, FormView, DetailView, TemplateView
 
from django.urls import reverse_lazy

from .forms import CustomUserCreationForm, SubscriptionForm

#import json
#from django.http import JsonResponse
#from django.views.decorators.csrf import csrf_exempt


# Create your views here.

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'



