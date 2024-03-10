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
from collections import defaultdict
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
    orders = Order.objects.all()

    name = request.GET.get('name')
    itemName = request.GET.get('item_name')
    quantity = request.GET.get('order_quantity')
    date_created = request.GET.get('date')
    date_returned = request.GET.get('returned_date')
    status = request.GET.get('status')
    released_by = request.GET.get('released_by')
    received_by = request.GET.get('returned_to')

    request.session['name'] = name
    request.session['item_name'] = itemName
    request.session['date'] = date_created
    request.session['returned_date'] = date_returned
    request.session['status'] = status
    request.session['released_by'] = released_by
    request.session['returned_to'] = received_by

    filters = {}

    if is_valid_queryparam(name):
        filters['name__icontains'] = name

    if is_valid_queryparam(itemName):
        filters['itemName__icontains'] = itemName
    
    if is_valid_queryparam(date_created):
        filters['date_created'] = date_created

    if is_valid_queryparam(date_returned):
        filters['date_returned'] = date_returned

    if is_valid_queryparam(status):
        filters['status'] = status

    if is_valid_queryparam(released_by):
        filters['released_by__icontains'] = released_by

    if is_valid_queryparam(received_by):
        filters['received_by__icontains'] = received_by

    ol = ol.filter(**filters)

    # Group orders by month and year
    grouped_orders = defaultdict(list)
    for order in ol:
        key = order.date_created.strftime('%Y-%m')  # Change the format as per your requirement
        grouped_orders[key].append(order)

    page = request.GET.get('page', 1)
    paginator = Paginator(ol, 30)

    try:
        ol = paginator.page(page)
    except PageNotAnInteger:
        ol = paginator.page(1)
    except EmptyPage:
        ol = paginator.page(paginator.num_pages)

    context = {
        'order_list': ol,
        'itemName': itemName,
        'quantity':quantity,
        'date_created':date_created,
        'date_returned':date_returned,
        'status':status,
        'released_by':released_by,
        'received_by':received_by,
        'grouped_orders': grouped_orders,  # Pass grouped orders to the template
        'orders' : orders
    }
    return render(request, 'dashboard/report.html', context)

def order_excel(request):
    ol = Order.objects.order_by('name')

    if 'name' in request.session:
        name = request.session['name']
    else:
        name = None

    if 'item_name' in request.session:
        itemName = request.session['item_name']
    else:
        itemName = None

    if 'date' in request.session:
        date_created = request.session['date']
    else:
        date_created = None

    if 'returned_date' in request.session:
        date_returned = request.session['returned_date']
    else:
        date_returned = None

    if 'status' in request.session:
        status = request.session['status']
    else:
        status = None

    if 'released_by' in request.session:
        released_by = request.session['released_by']
    else:
        released_by = None

    if 'returned_to' in request.session:
        received_by = request.session['returned_to']
    else:
        received_by = None

    

    if is_valid_queryparam(name):
        ol = ol.filter(name__icontains=name)

    if is_valid_queryparam(itemName):
        ol = ol.filter(itemName__icontains=itemName)
    
    if is_valid_queryparam(date_created):
        ol = ol.filter(date_created=date_created)

    if is_valid_queryparam(date_returned):
        ol = ol.filter(date_returned=date_returned)

    if is_valid_queryparam(status):
        ol = ol.filter(status=status)

    if is_valid_queryparam(released_by):
        ol = ol.filter(released_by__icontains=released_by)

    if is_valid_queryparam(received_by):
        ol = ol.filter(received_by__icontains=received_by)

    if name is None or name == '':
        name = "All Orders"
    else:
        name = name

    if itemName is None or name == '':
        itemName = "All Items"
    else:
        itemName = itemName
    
    if date_created is None or date_created == '':
        date_created = "2024 - 2090"
    else:
        date_created = date_created

    if date_returned is None or date_returned == '':
        date_returned = "2024 - 2090"
    else:
        date_returned = date_returned

    if status is None or status == '':
        status = "All Status"
    else:
        status = status

    if released_by is None or released_by == '':
        released_by = "All Admins"
    else:
        released_by = released_by

    if received_by is None or received_by == '':
        received_by = "All Admins"
    else:
        received_by = received_by

    

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',)
    response['Content-Disposition'] = 'attachment; filename="' + 'Order Report' +'.xlsx"'
    workbook = Workbook()

    worksheet = workbook.active

    worksheet.merge_cells('A1:H1')
    worksheet.merge_cells('A2:h22')
    first_cell = worksheet['A1']
    first_cell.value = "Order List" + "From " + date_created
    first_cell.fill = PatternFill("solid", fgColor="246ba1")
    first_cell.font  = Font(bold=True, color="F7F6FA")
    first_cell.alignment = Alignment(horizontal="center", vertical="center")

    second_cell = worksheet['A2']
    second_cell.value = name
    second_cell.font  = Font(bold=True, color="246ba1")
    second_cell.alignment = Alignment(horizontal="center", vertical="center")

    worksheet.title = 'Order List List' + " " + date_created

    # Define the titles for columns
    columns = ['Username','Item Name','Quantity', 'Date Created', 'Date Received', 'Status', 'Released By', 'Received By']
    row_num = 3

    # Assign the titles for each cell of the header
    for col_num, column_title in enumerate(columns, 1):
        cell = worksheet.cell(row=row_num, column=col_num)
        cell.value = column_title
        cell.fill = PatternFill("solid", fgColor="50C878")
        cell.font  = Font(bold=True, color="F7F6FA")
        third_cell = worksheet['D3']
        third_cell.alignment = Alignment(horizontal="right")

    for orders in ol:
        row_num += 1

        # Define the data for each cell in the row
        row = [orders.users.username,orders.item_name.name,orders.order_quantity,orders.date,orders.returned_date,orders.status,orders.released_by,orders.returned_to]

        # Assign the data for each cell of the row
        for col_num, cell_value in enumerate(row, 1):
            cell = worksheet.cell(row=row_num, column=col_num)
            cell.value = cell_value
            if isinstance(cell_value, decimal.Decimal):
                cell.number_format = numbers.FORMAT_NUMBER_COMMA_SEPARATED1

    workbook.save(response)
    return response