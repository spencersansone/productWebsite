from django.contrib import admin
from .models import *

class ProductList(admin.ModelAdmin):
    list_display = ('title','product_price','shipping_price','description',)
    ordering = ['id']
admin.site.register(Product, ProductList)

# Register your models here.
