from django.shortcuts import render
import requests
import json

from UdemyDjangoStock import settings

def home(request):
    api_key = settings.API_KEY
    print("API_KEY", api_key)

    api_request = requests.get(f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey={api_key}')
    try:
        result = json.loads(api_request.content)
    except Exception as e:
        print("API request failed", e)
        result = f"API request failed - {e}"

    return render(request, 'home.html', {'api': result,
                                         'symbol':result["Meta Data"]["2. Symbol"]
                                         })

def about(request):
    return render(request, 'about.html', {})