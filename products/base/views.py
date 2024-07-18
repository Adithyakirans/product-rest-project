from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Products
from .serializers import ProductSerializer
# Create your views here.

class ProductView(APIView):
    def get(self,request,*args,**kwargs):
        qs = Products.objects.all()
        serializer= ProductSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    def post(self,request,*args,**kwargs):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            Products.objects.create(**serializer.validated_data)
            return Response(data=serializer.data)
        else:
            return Response(serializer.errors)
        
class ProductDetailView(APIView):
    def get(self,request,*args,**kwargs):
        id = kwargs.get('id')
        qs = Products.objects.get(id=id)
        serializer = ProductSerializer(qs,many=False)
        return Response(data=serializer.data)
    
    def delete(self,request,*args,**kwargs):
        id = kwargs.get('id')
        qs = Products.objects.get(id=id).delete()
        return Response(data={'msg':'deleted'})