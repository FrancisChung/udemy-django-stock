from typing import Any
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, redirect
from .forms import StockForm
from django.contrib import messages
import requests
import json

from requests import Response

from UdemyDjangoStock import settings
from quotes.models import Stock

none_ticker_error = f"Error - API request failed - None passed as Ticker"

def extract_ticker(request: WSGIRequest | Any) -> str | Any:
    if request.method == "POST":
        ticker = request.POST.get("ticker")
        print("ticker:", ticker)
        result = search_ticker(ticker)
    else:
        result = search_ticker("IBM")
    return result


def extract_prices(result: str) -> list[dict[str, str]]:
    if result == none_ticker_error:
        return [{
            'date': 'None',
            'opening_price': 'None',
            'closing_price': 'None'
        }]
    daily_prices = [
        {
            'ticker': result['Meta Data']['2. Symbol'],
            'date': date,
            'opening_price': data['1. open'],
            'closing_price': data['4. close']
        }
        for date, data in result['Time Series (Daily)'].items()
    ]
    return daily_prices


def search_ticker(ticker: str = "IBM"):
    if ticker == "None":
        ticker = "IBM"

    print("ticker:", ticker)
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

def home(request):
    result = extract_ticker(request)

    daily_prices = extract_prices(result)

    return render(request, 'home.html', {'api': result,
                                         'symbol': result["Meta Data"]["2. Symbol"],
                                         'prices': daily_prices
                                         })

def add_stock(requRefest):
    if request.method == 'POST':
        form = StockForm(request.POST or None)
        messages.success(request, 'Finding Stock and Saving')
        if form.is_valid():
            messages.success(request, 'Saving Stock')
            form.save()
            messages.success(request, 'Stock has been added')
            return redirect('add_stock')
        else:
            messages.success(request, 'Errors in form')
    else:
        messages.success(request, 'Retrieving all the stocks in DB')
        ticker = Stock.objects.all()
        return render(request, 'add_stock.html', {'ticker': ticker})

def about(request):
    return render(request, 'about.html', {})