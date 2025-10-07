from django.shortcuts import render
import requests
import json

from requests import Response

from UdemyDjangoStock import settings

none_ticker_error = f"Error - API request failed - None passed as Ticker"

def home(request):
    if request.method == "POST":
        ticker = request.POST.get("ticker");
        print("ticker:", ticker)
        result = search_ticker(ticker)
    else:
        result = search_ticker("IBM")

    daily_prices = extract_prices(result)

    return render(request, 'home.html', {'api': result,
                                         'symbol': result["Meta Data"]["2. Symbol"],
                                         'prices': daily_prices
                                         })


def extract_prices(result: str | Any) -> list[dict[str, Any]]:
    if result == none_ticker_error:
        return [{
            'date': 'None',
            'opening_price': 'None',
            'closing_price': 'None'
        }]
    daily_prices = [
        {
            'date': date,
            'opening_price': data['1. open'],
            'closing_price': data['4. close']
        }
        for date, data in result['Time Series (Daily)'].items()
    ]
    return daily_prices


def search_ticker(ticker: str = "IBM"):
    if ticker == "None":
        result = none_ticker_error
        return result

    api_key = settings.API_KEY
    print("API_KEY", api_key)

    api_request = requests.get(
        f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={api_key}')
    try:
        result = json.loads(api_request.content)
    except Exception as e:
        print("API request failed", e)
        result = f"Error - API request failed - {e}"

    return result


def about(request):
    return render(request, 'about.html', {})