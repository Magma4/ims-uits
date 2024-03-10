from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import *
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from openpyxl import Workbook
from openpyxl.styles import *
import decimal
# Create your views here.


@login_required(login_url='user-login')
def dashboard(request):
    user = request.user
    orders = Order.objects.all()
    items = Stock.objects.all()
    order_count = Order.objects.filter(users=user).count()
    
    context = {
        'orders' : orders,
        'order_count': order_count,
        'items' : items
    }
    
    return render(request, 'dashboard/dashboard.html', context)

@login_required
def stock(request):
    items = Stock.objects.all()
    orders = Order.objects.all()


    if request.method == 'POST':
        form = StockForm(request.POST)
        if form.is_valid():
            form.save()
            stock_name = form.cleaned_data.get('name')
            messages.success(request, f'{stock_name} has been added.')
            return redirect('stock')
    else:
        form = StockForm()
    mydictionary = {
        "stocks" : items,
        "form" : form,
        "orders" : orders
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
            order_quantity = instance.order_quantity
            stock_quantity = instance.item_name.quantity
            if order_quantity <= stock_quantity:
                instance.save()
                return redirect('dashboard')
            else:
                messages.error(request, "Order quantity cannot be more than stock quantity")
                return redirect('requisition')  # Redirect back to the requisition page
    else:
        form = OrderForm()
    context = {
        'orders': orders,
        'form': form,
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
        
        # Check if the status is being changed to 'released'
        if new_status == 'released':
            order.status = new_status
            order.released_by = request.user.username  # Set the released_by field to the username of the admin
            order.save()
            messages.success(request, f"Order {order.id} has been released by {request.user.username}.")
        elif new_status == 'returned':
            order.status = new_status
            order.returned_to = request.user.username  # Set the returned_to field to the username of the admin
            order.save()
            messages.success(request, f"Order {order.id} has been marked as returned by {request.user.username}.")
        else:
            order.status = new_status
            order.save()
            messages.success(request, f"Order {order.id} status has been updated.")
    
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
            instance = form.save(commit=False)
            # Retrieve the current stock quantity
            current_stock_quantity = instance.item_name.quantity
            # Check if the order status is released and the new order quantity exceeds the current stock quantity
            if instance.status == 'pending' and instance.order_quantity > current_stock_quantity:
                # Add an error message if the condition is met
                messages.error(request, "Insufficient stock quantity")
            else:
                instance.save()
                if request.user.is_superuser:
                    return redirect('requisition')
                else:
                    return redirect('dashboard')
    else:
        form = OrderForm(instance=order)
    context = {
        'form': form,
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

def is_valid_queryparam(param):
    return param != '' and param is not None

def report(request):
    ol = Order.objects.order_by('users')

    name = request.GET.get('name')
    itemName = request.GET.get('item_name')
    date_created = request.GET.get('date')
    date_returned = request.GET.get('returned_date')
    year = request.GET.get('year')
    status = request.GET.get('status')

    request.session['name'] = name
    request.session['year'] = year

    if is_valid_queryparam(name):
        qs = qs.filter(name__icontains=name)

    if is_valid_queryparam(year):
        qs = qs.filter(year=year)

    page = request.GET.get('page', 1)
    paginator = Paginator(qs, 30)

    try:
        qs = paginator.page(page)
    except PageNotAnInteger:
        qs = paginator.page(1)
    except EmptyPage:
        qs = paginator.page(paginator.num_pages)

    context = {
        'countries_list': qs,
        'name': name,
        'year':year,
    }
    return render(request, 'dashboard/report.html')

