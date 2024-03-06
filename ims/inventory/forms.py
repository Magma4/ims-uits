from django import forms
from .models import *

class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['name', 'description', 'quantity' ]

from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['item_name', 'order_description', 'order_quantity']

