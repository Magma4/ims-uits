from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import *
# Create your views here.


@login_required(login_url='user-login')
def dashboard(request):
    
    return render(request, 'dashboard/dashboard.html')

@login_required
def stock(request):
    items = Stock.objects.all()

    if request.method == 'POST':
        form = StockForm(request.POST)
    else:
        form = StockForm()
    mydictionary = {
        "stocks" : items,
        "form" : form
    }
    return render(request, 'dashboard/stock.html', context=mydictionary)

@login_required
def requisition(request):
    
    return render(request, 'dashboard/requisition.html')

@login_required
def employees(request):
    return render(request, 'dashboard/employees.html')

@login_required
def trying(request):
    return render(request, 'dashboard/try.html')


