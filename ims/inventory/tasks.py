from celery import shared_task
from django.core.mail import send_mail
from .models import Order
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_reminder_emails():
    today = timezone.localdate()
    tomorrow = today + timezone.timedelta(days=1)

    orders_due_today = Order.objects.filter(intended_date_of_return=today, status__in=['pending', 'released'])
    orders_due_tomorrow = Order.objects.filter(intended_date_of_return=tomorrow, status__in=['pending', 'released'])
    overdue_orders = Order.objects.filter(intended_date_of_return__lt=today, status__in=['pending', 'released'])

    logger.info(f"Orders due today: {orders_due_today.count()}")
    logger.info(f"Orders due tomorrow: {orders_due_tomorrow.count()}")
    logger.info(f"Overdue orders: {overdue_orders.count()}")

    # Send emails for each case, adding logging to see if emails are actually attempted to be sent
    for order in orders_due_today:
        send_mail(
            'Reminder: Your Order Return is Due Today',
            f'Dear {order.users.username}, your order {order.item_name.name} is due to be returned today.',
            'from@example.com',
            [order.users.email],
            fail_silently=False,
        )
        logger.info(f"Sent due today email to {order.users.email}")

    for order in orders_due_tomorrow:
        send_mail(
            'Reminder: Your Order Return is Due Tomorrow',
            f'Dear {order.users.username}, your order {order.item_name.name} is due to be returned tomorrow.',
            'from@example.com',
            [order.users.email],
            fail_silently=False,
        )
        logger.info(f"Sent due tomorrow email to {order.users.email}")

    for order in overdue_orders:
        send_mail(
            'Urgent Reminder: Your Order Return is Overdue',
            f'Dear {order.users.username}, your order {order.item_name.name} was due to be returned on {order.intended_date_of_return}. Please return it immediately to avoid penalties.',
            'from@example.com',
            [order.users.email],
            fail_silently=False,
        )
        logger.info(f"Sent overdue email to {order.users.email}")
