from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from model_utils.fields import MonitorField
from model_utils import FieldTracker

class Stock(models.Model):
    name = models.CharField(max_length=100, null=True)
    description = models.CharField(max_length=200, null=True)
    quantity = models.PositiveIntegerField(null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name_plural = 'Stock'   

    def __str__(self):
        return f'{self.name}'
    
    def get_total_quantity(self):
        total_quantity = self.quantity
        orders = Order.objects.filter(item_name=self)
        for order in orders:
            if order.status == 'released':
                total_quantity -= order.request_quantity
            elif order.status == 'returned':
                total_quantity == total_quantity
        return total_quantity
    

    
class Order(models.Model):
    STATUS_CHOICES = (
        ('released', 'Released'),
        ('pending', 'Pending'),
        ('returned', 'Returned'),
    )
    item_name = models.ForeignKey(Stock, on_delete=models.CASCADE, null=True)
    users = models.ForeignKey(User, models.CASCADE, null=True)
    request_quantity = models.PositiveIntegerField(null=True)
    issued_to = models.CharField(max_length=200, null=True, blank=users)
    request_description = models.CharField(max_length=300, null=True)
    date = models.DateTimeField(auto_now_add=True)
    returned_date = models.DateTimeField(null=True, blank=True)  # New field for returned date
    intended_date_of_return = models.DateField(null=True, blank=True)
    approved_by = models.CharField(max_length=100, null=True)
    released_by = models.CharField(max_length=100, null=True)
    returned_to = models.CharField(max_length=100, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    status_changed = MonitorField(monitor='status')
    tracker = FieldTracker()

    class Meta:
        verbose_name_plural = 'Order'

    def __str__(self):
        if self.users:
            username = self.users.username
        else:
            username = "Unknown User"
        return f'{self.request_quantity} - {self.item_name.name} ordered by {username} on {self.date} (Status: {self.get_status_display()})'

    def save(self, *args, **kwargs):
        if self.status == 'returned':
            self.item_name.save()
            # Set returned date
            self.returned_date = timezone.now()
        super().save(*args, **kwargs)

        