from celery import shared_task
from django.core.mail import send_mail
from .models import Order
from django.utils import timezone

@shared_task
def send_reminder_emails():
    today = timezone.localdate()
    tomorrow = today + timezone.timedelta(days=1)

    # Orders due today
    orders_due_today = Order.objects.filter(intended_date_of_return=today, status__in=['pending', 'released'])
    for order in orders_due_today:
        send_mail(
            'Reminder: Your Order Return is Due Today',
            f'Dear {order.users.username}, your order {order.item_name.name} is due to be returned today.',
            'from@example.com',
            [order.users.email],
            fail_silently=False,
        )

    # Orders due tomorrow
    orders_due_tomorrow = Order.objects.filter(intended_date_of_return=tomorrow, status__in=['pending', 'released'])
    for order in orders_due_tomorrow:
        send_mail(
            'Reminder: Your Order Return is Due Tomorrow',
            f'Dear {order.users.username}, your order {order.item_name.name} is due to be returned tomorrow.',
            'from@example.com',
            [order.users.email],
            fail_silently=False,
        )

    # Overdue orders
    overdue_orders = Order.objects.filter(intended_date_of_return__lt=today, status__in=['pending', 'released'])
    for order in overdue_orders:
        send_mail(
            'Urgent Reminder: Your Order Return is Overdue',
            f'Dear {order.users.username}, your order {order.item_name.name} was due to be returned on {order.intended_date_of_return}. Please return it immediately to avoid penalties.',
            'from@example.com',
            [order.users.email],
            fail_silently=False,
        )
