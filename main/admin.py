from django.contrib import admin
from .models import *

class ProductList(admin.ModelAdmin):
    list_display = ('title','product_price','shipping_price','description',)
    ordering = ['id']
admin.site.register(Product, ProductList)

class UserProfileList(admin.ModelAdmin):
    list_display = ('user',)
    ordering = ['user']
admin.site.register(UserProfile, UserProfileList)

class SignUpAttemptList(admin.ModelAdmin):
    list_display = ('id','first_name',)
    ordering = ['id']
admin.site.register(SignUpAttempt, SignUpAttemptList)

# Register your models here.
