from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Order
from django.utils import timezone
import datetime

@receiver(post_save, sender=Order)
def check_order_return_dates(sender, instance, created, **kwargs):
    # When order is first created, do not send an email
    if created:
        return

    # Check if today is one day before the intended date of return
    if instance.intended_date_of_return == timezone.now().date() + datetime.timedelta(days=1):
        send_mail(
            subject='Reminder: Your return date is tomorrow',
            message=f'Hi {instance.users.first_name}, your order for {instance.item_name} is due to be returned tomorrow.',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[instance.users.email],
            fail_silently=False,
        )

    # Check if today is the intended date of return
    if instance.intended_date_of_return == timezone.now().date():
        send_mail(
            subject='Notice: Your return date is today',
            message=f'Hi {instance.users.first_name}, your order for {instance.item_name} is due to be returned today.',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[instance.users.email],
            fail_silently=False,
        )

@receiver(post_save, sender=Order)
def check_order_status_changes(sender, instance, created, **kwargs):
    if created:
        return  # If the record is new, do nothing

    # Check if the order status has changed to 'returned'
    if instance.status == 'returned' and instance.returned_date is None:
        instance.returned_date = timezone.now()
        instance.save()
        send_mail(
            subject='Order Returned',
            message=f'Hi {instance.users.first_name}, your order for {instance.item_name} has been marked as returned.',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[instance.users.email],
            fail_silently=False,
        )

