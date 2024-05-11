from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Order

@receiver(post_save, sender=Order)
def send_status_update_email(sender, instance, created, **kwargs):
    if not created and instance.tracker.has_changed('status'):
        send_mail(
            'Order Status Updated',
            f'Hello {instance.users.username}, the status of your order for {instance.item_name.name} has been updated from {instance.tracker.previous("status")} to {instance.status}.',
            'uitsims24@gmail.com',
            [instance.users.email],
            fail_silently=False,
        )
        print(f"Email sent for order {instance.id} status update from {instance.tracker.previous('status')} to {instance.status}")