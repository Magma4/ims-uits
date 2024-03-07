from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import *
from django.contrib.auth.models import User
from django.db.models import Q
# Create your views here.


@login_required(login_url='user-login')
def dashboard(request):
    user = request.user
    orders = Order.objects.all()
    order_count = Order.objects.filter(users=user).count()
    
    context = {
        'orders' : orders,
        'order_count': order_count,
    }
    
    return render(request, 'dashboard/dashboard.html', context)

@login_required
def stock(request):
    items = Stock.objects.all()

    if request.method == 'POST':
        form = StockForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('stock')
    else:
        form = StockForm()
    mydictionary = {
        "stocks" : items,
        "form" : form
    }
    return render(request, 'dashboard/stock.html', context=mydictionary)

@login_required
def requisition(request):
    orders = Order.objects.all()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.users = request.user
            instance.save()
            return redirect('dashboard')
    else:
        form = OrderForm()
    context = {
        'orders' : orders,
        'form' : form,
        
    }
    
    return render(request, 'dashboard/requisition.html', context)

@login_required
def employees(request):
    workers = User.objects.all()
    context={
        'workers' : workers
    }
    return render(request, 'dashboard/employees.html', context)


@login_required
def stock_delete(request, pk):
    item = Stock.objects.get(id=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('stock')
    return render(request, 'dashboard/stock_delete.html')

@login_required
def stock_update(request, pk):
    item = Stock.objects.get(id=pk)
    if request.method == 'POST':
        form = StockForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('stock')
    else:
        form = StockForm(instance=item)
    context = {
        'form' : form
    }
    return render(request, 'dashboard/stock_update.html', context)

@login_required
def employees_detail(request, pk):
    workers = User.objects.get(id=pk)
    context={
        'workers' : workers,
    }

    return render(request, 'dashboard/employees_detail.html', context)

@login_required
def update_order_status(request, order_id):
    if request.method == 'POST' and request.user.is_superuser:
        order = Order.objects.get(id=order_id)
        new_status = request.POST.get('status')
        order.status = new_status
        order.save()    
    return redirect('requisition')

@login_required
def delete_order(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':       
        order.delete()
        if request.user.is_superuser:
            return redirect('requisition')
        else:
            return redirect('dashboard')
    return render(request, 'dashboard/order_delete.html')

@login_required
def order_update(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            if request.user.is_superuser:
                return redirect('requisition')
            else:
                return redirect('dashboard')
    else:
        form = OrderForm(instance=order)
    context = {
        'form' : form,
    }
    return render(request, 'dashboard/order_update.html', context)

def list_requisition(request):
    return render(request, 'dashboard/list_requisition.html')

def searchdata(request):
    q = request.GET.get('query') # Get the query parameter from the request
    if q:
        orders = Order.objects.filter(Q(users__username__icontains=q) | Q(order_description__icontains=q) | Q(users__first_name__icontains=q) | Q(users__last_name__icontains=q))
    else:
        orders = Order.objects.all()

    context = {
        "orders": orders,
    }
    return render(request, 'dashboard/requisition.html', context=context)

def searchdata2(request):
    q = request.GET.get('query') # Get the query parameter from the request
    if q:
        workers = User.objects.filter(Q(username__icontains=q) | Q(first_name__icontains=q) | Q(last_name__icontains=q))
    else:
        workers = User.objects.all()

    context = {
        "workers": workers,
    }
    return render(request, 'dashboard/employees.html', context=context)

def searchdata3(request):
    q = request.GET.get('query')  # Get the query parameter from the request
    if q:
        stocks = Stock.objects.filter(Q(name__icontains=q) | Q(description__icontains=q))
    else:
        stocks = Stock.objects.all()

    context = {
        "stocks": stocks,
    }
    return render(request, 'dashboard/stock.html', context=context)


