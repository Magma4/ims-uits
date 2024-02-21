from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

# Create your views here.
def index(request):
    return render(request, 'index.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def stock(request):
    return render(request, 'stock.html')

def requisition(request):
    return render(request, 'requisition.html')

def employees(request):
    return render(request, 'employees.html')

def register(request):
    return render(request, 'register.html')
