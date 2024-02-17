from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

# Create your views here.
def index(request):
    return render(request, 'index.html')

def stock(request):
    return render(request, 'stock.html')
