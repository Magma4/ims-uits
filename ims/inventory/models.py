from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Stock(models.Model):
    name = models.CharField(max_length=100, null=True)
    description = models.CharField(max_length=200, null=True)
    quantity = models.PositiveIntegerField(null=True)

    def __str__(self):
        return f'{self.name}-{self.quantity}'
    
class Order(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, null=True)
    Users = models.ForeignKey(User, models.CASCADE, null=True )
    order_quantity = models.PositiveIntegerField(null=True)
    order_description = models.CharField(max_length=200, null=True)
    date = models.DateTimeField(auto_now_add=True)

