from django import forms
from .models import *

class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['name', 'description', 'quantity' ]