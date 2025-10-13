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

def extract_unique_tickers(stock_data):
    unique_tickers = [{'ticker': ticker} for ticker in set(item['ticker'] for item in stock_data)]
    print("unique_tickers:", unique_tickers)
    return unique_tickers


def extract_prices(result: str) -> list[dict[str, str]]:
    if result == none_ticker_error:
        return [{
            'date': 'None',
            'opening_price': 'None',
            'closing_price': 'None'
        }]

    print("result", result)

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
        f'https://api.twelvedata.com/time_series?symbol={ticker}&interval=1day&apikey={api_key}')
    try:
        result = json.loads(api_request.content)
    except Exception as e:
        print("API request failed", e)
        result = f"Error - API request failed - {e}"

    return result

def home(request):
    return redirect(add_stock)
    # result = extract_ticker(request)
    # return render(request, 'home.html', {'data': result })

def add_stock(request):
    if request.method == 'POST':
        results = extract_ticker(request)
        transformed = dto_to_db(results)
        for item in transformed:
            form = StockForm(item)
            if form.is_valid():
                form.save()
        messages.success(request, 'Stock has been added')
        return redirect('add_stock')
    else:
        print('request method', request.method)
        messages.success(request, 'Retrieving all the stocks in DB')
        ticker = Stock.objects.values()
        print("ticker from db", ticker)
        return render(request, 'add_stock.html', {'db': ticker})


def delete_stock(request):
    ticker = Stock.objects.values()
    unique_tickers = extract_unique_tickers(ticker)
    return render(request, "delete_stock.html", {'db': unique_tickers})


def dto_to_db(input) -> Any:
    ticker = input.get("meta", {}).get("symbol", "N/A")
    values = input.get("values", [])

    dto_list = []
    for v in values:
        dto_list.append({
            "ticker": ticker,
            "date": v.get("datetime"),
            "opening_price": v.get("open", 0),
            "closing_price": v.get("close", 0)
        })
    return dto_list


def delete(request, stock_id):
    item = Stock.objects.get(id=stock_id)
    item.delete()

    messages.success(request, 'Stock has been deleted')
    return redirect(add_stock)

def delete_ticker(request, ticker):
    items = Stock.objects.filter(ticker=ticker)
    items.delete()

    messages.success(request, f'Ticker {ticker} has been deleted')
    return redirect(delete_stock)


def about(request):
    return render(request, 'about.html', {})