from celery import shared_task
from django.core.mail import send_mail
from .models import Order
from django.utils import timezone
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_reminder_emails():
    today = timezone.localdate()
    tomorrow = today + timezone.timedelta(days=1)

    orders_due_today = Order.objects.filter(intended_date_of_return=today, status__in=['released'])
    orders_due_tomorrow = Order.objects.filter(intended_date_of_return=tomorrow, status__in=['released'])
    overdue_orders = Order.objects.filter(intended_date_of_return__lt=today, status__in=['released'])

    logger.info(f"Orders due today: {orders_due_today.count()}")
    logger.info(f"Orders due tomorrow: {orders_due_tomorrow.count()}")
    logger.info(f"Overdue orders: {overdue_orders.count()}")

    for order in orders_due_today:
        mail_subject = 'Reminder: Your Order Return is Due Today'
        message = f'Dear {order.users.username}, your order {order.item_name.name} is due to be returned today.'
        to_email = order.users.email
        send_mail(
            subject= mail_subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[to_email],
            fail_silently=True,
        )
        
        logger.info(f"Sent due today email to {order.users.email}")

    for order in orders_due_tomorrow:
        mail_subject = 'Reminder: Your Order Return is Due Tomorrow'
        message = f'Dear {order.users.username}, your order {order.item_name.name} is due to be returned tomorrow.'
        to_email = order.users.email
        send_mail(
            subject= mail_subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[to_email],
            fail_silently=True,
        )
        logger.info(f"Sent due tomorrow email to {order.users.email}")

    for order in overdue_orders:
        mail_subject = 'Urgent Reminder: Your Order Return is Overdue'
        message = f'Dear {order.users.username}, your order {order.item_name.name} was due to be returned on {order.intended_date_of_return}. Please return it immediately to avoid penalties.'
        to_email = order.users.email
        send_mail(
            subject= mail_subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[to_email],
            fail_silently=True,
        )
        logger.info(f"Sent overdue email to {order.users.email}")

    return "Done"
