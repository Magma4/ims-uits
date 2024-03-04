from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Stock(models.Model):
    name = models.CharField(max_length=100, null=True)
    description = models.CharField(max_length=200, null=True)
    quantity = models.PositiveIntegerField(null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Stock'

    def __str__(self):
        return f'{self.name}-{self.quantity}-{self.date_created}-{self.user}'
    
class Order(models.Model):
    STATUS_CHOICES = (
        ('released', 'Released'),
        ('pending', 'Pending'),
        ('returned', 'Returned'),
        ('approved', 'Approved'),
    )
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, null=True)
    users = models.ForeignKey(User, models.CASCADE, null=True )
    order_quantity = models.PositiveIntegerField(null=True)
    order_description = models.CharField(max_length=200, null=True)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    class Meta:
        verbose_name_plural = 'Order'

    def __str__(self):
        return f'{self.order_quantity} {self.stock} ordered by {self.users.username} on {self.date} (Status: {self.get_status_display()})' 
    
