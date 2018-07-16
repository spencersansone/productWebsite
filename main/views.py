from django.shortcuts import render, get_object_or_404
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views import generic



class ProductList(generic.ListView):
    
    template_name = 'main/productList.html'
    context_object_name = 'productList'
    
    def get_queryset(self):
        return Product.objects.all()
        
class ProductAPIList(APIView):
    
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
# Create your views here.
