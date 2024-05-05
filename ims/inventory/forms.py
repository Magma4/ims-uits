from django import forms
from .models import *
from bootstrap_modal_forms.forms import BSModalModelForm
from .models import Order
class StockForm(BSModalModelForm):
    class Meta:
        model = Stock
        fields = ['name', 'description', 'quantity' ]



class OrderForm(BSModalModelForm):
    class Meta:
        model = Order
        fields = ['item_name', 'order_description', 'order_quantity']

