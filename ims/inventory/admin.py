from django.contrib import admin
from .models import Stock

admin.site.site_header = 'UITS INVENTORY ADMINISTRATION'

class StockAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'quantity')
    list_filter = ('name',)

# Register your models here.
admin.site.register(Stock, StockAdmin )
