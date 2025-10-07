from django import forms
from .models import Stock

class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['ticker', 'date', 'opening_price', 'closing_price']