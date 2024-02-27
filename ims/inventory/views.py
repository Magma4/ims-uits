from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

# Create your views here.


def dashboard(request):
    return render(request, 'dashboard/dashboard.html')

def stock(request):
    return render(request, 'dashboard/stock.html')

def requisition(request):
    return render(request, 'dashboard/requisition.html')

def employees(request):
    return render(request, 'dashboard/employees.html')

def trying(request):
    return render(request, 'dashboard/try.html')

def profile(request):
    return render(request, 'dashboard/profile.html')
