from django.shortcuts import render
import requests
import json

from requests import Response

from UdemyDjangoStock import settings

def home(request):


    if request.method == "POST":
        ticker = request.POST['ticker']
        "do something"
    else:
        "do something else"

    api_request = search_ticker(api_key)
    try:
        result = json.loads(api_request.content)
    except Exception as e:
        print("API request failed", e)
        result = f"API request failed - {e}"

    daily_prices = [
        {
            'date': date,
            'opening_price': data['1. open'],
            'closing_price': data['4. close']
        }
        for date, data in result['Time Series (Daily)'].items()
    ]

    return render(request, 'home.html', {'api': result,
                                         'symbol': result["Meta Data"]["2. Symbol"],
                                         'prices': daily_prices
                                         })


def search_ticker(ticker: str = "IBM") -> Response:
    api_key = settings.API_KEY
    print("API_KEY", api_key)

    api_request = requests.get(
        f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={api_key}')
    return api_request


def about(request):
    return render(request, 'about.html', {})