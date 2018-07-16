from django.contrib import admin
from .models import *

class ProductList(admin.ModelAdmin):
    list_display = ('id',)
    ordering = ['id']
admin.site.register(Product, ProductList)

# Register your models here.
