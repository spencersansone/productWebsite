from django.shortcuts import render
from .models import *
from django.views import generic

class ProductList(generic.ListView):
    template_name = 'main/productList.html'
    context_object_name = 'productList'
    
    def get_queryset(self):
        return Product.objects.all()

# Create your views here.
