from django.shortcuts import render
from django.views.generic import TemplateView
import requests
from .forms import CityForm  # Import the form
from django.conf import settings
from .utils import get_weather



class HomePageView(TemplateView):
    template_name = "home.html"



    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        
        # Initialize the form
        form = CityForm()
        
        # Default weather data (for example, for "London")
        weather = None
        city = "London"  # Default city
        
        # If it's a GET request with a city selected, fetch the weather
        if self.request.GET.get("city"):
            city = self.request.GET.get("city")
            weather = get_weather(city, settings.OPENWEATHERMAP_API_KEY)
        
        # Add the weather data and form to the context
        context['weather'] = weather
        context['city'] = city
        context['form'] = form
        return context



    



    

