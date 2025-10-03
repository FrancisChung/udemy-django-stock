from django.shortcuts import render
import requests
import json

from UdemyDjangoStock import settings

# Create your views here.
def home(request):
    api_key = settings.API_KEY
    print("API_KEY", api_key)

    # api_request = requests.get('https://quotes.sina.com')

    return render(request, 'home.html', {})

def about(request):
    return render(request, 'about.html', {})