from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

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

    
class Order(models.Model):
    STATUS_CHOICES = (
        ('released', 'Released'),
        ('pending', 'Pending'),
        ('returned', 'Returned'),
    )
    item_name = models.ForeignKey(Stock, on_delete=models.CASCADE, null=True)
    users = models.ForeignKey(User, models.CASCADE, null=True)
    order_quantity = models.PositiveIntegerField(null=True)
    order_description = models.CharField(max_length=200, null=True)
    date = models.DateTimeField(auto_now_add=True)
    returned_date = models.DateTimeField(null=True, blank=True)  # New field for returned date
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    class Meta:
        verbose_name_plural = 'Order'

    def __str__(self):
        if self.users:
            username = self.users.username
        else:
            username = "Unknown User"
        return f'{self.order_quantity} - {self.item_name.name} ordered by {username} on {self.date} (Status: {self.get_status_display()})'

    def save(self, *args, **kwargs):
        if self.status == 'released':
            # Deduct quantity from stock
            self.item_name.quantity -= self.order_quantity
            self.item_name.save()
        elif self.status == 'returned':
            # Add quantity to stock
            self.item_name.quantity += self.order_quantity
            self.item_name.save()
            # Set returned date
            self.returned_date = timezone.now()
        super().save(*args, **kwargs)