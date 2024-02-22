from django.contrib import admin
from .models import *

admin.site.site_header = 'UITS INVENTORY ADMINISTRATION'

class StockAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'quantity')
    list_filter = ('name',)


# class OrderAdmin(admin.ModelAdmin):
#     list_display = ('name', 'firr')

# Register your models here.
admin.site.register(Stock, StockAdmin )
admin.site.register(Order)
