from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Products
from .serializers import ProductSerializer,UserSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from django.contrib.auth.models import User
# Create your views here.


# --------using API view-----------------------------------------------------------------------
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
    
    def put(self,request,*args,**kwargs):
        id = kwargs.get('id')
        Products.objects.filter(id=id).update(**request.data)
        qs = Products.objects.get(id=id)
        serializer = ProductSerializer(qs,many=False)
        return Response(data=serializer.data)
    
#  ------------USING VIEWSETS--------------------------------------------------------------------------------
    # methods for each functions
    # all methods can be done in 1 view


# class ProductViewsetView(viewsets.ViewSet):
#     def list(self,request,*args,**kwargs):
#         qs = Products.objects.all()
#         serializer = ProductSerializer(qs,many=True)
#         return Response(data=serializer.data)
    
#     def create(self,request,*args,**kwargs):
#         serializer = ProductSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(data=serializer.data)
#         else:
#             return Response(serializer.errors)
    
#     def retrieve(self,request,*args,**kwargs):
#         # get the id of data passed by the clients here id is pk
#         id = kwargs.get('pk')
#         qs = Products.objects.get(id=id)
#         serializer = ProductSerializer(qs,many=False)
#         return Response(data=serializer.data)
    
#     def destroy(self,request,*args,**kwargs):
#         # get the id of data passed by the clients here id is pk
#         id = kwargs.get('pk')
#         qs = Products.objects.get(id=id).delete()
#         return Response(data='deleted')
    
#     def update(self,request,*args,**kwargs):
#         # get id of data we want to update
#         id = kwargs.get('pk')
#         # get data from the table using id
#         obj = Products.objects.get(id=id)
#         # serialize the data
#         # here we get the data we want to update with ie , request.data
#         # obj is the data we want to update,so instance=obj

#         serializer = ProductSerializer(data=request.data,instance=obj)
        
#         if serializer.is_valid():
#             serializer.save()
#             return Response(data=serializer.data)
#         else:
#             return Response(data=serializer.errors)
        
# getting category
# we can create methods for ourself other than built in methods

@action(methods=['GET'],detail=False)
def categories(self,request,*args,**kwargs):
    res = Products.objects.values_list('category',flat=True).distinct
    # flat = True ==> get a list
    # .distinct ==> same category womt repeat
    return Response(data=res)
    # as it is value list and not queryset no need to serialize the data


# class UserView(viewsets.ViewSet):
#     def create(self,request,*args,**kwargs):
#         # serialize data in to python native
#         serializer = UserSerializer(data=request.data)
#         # check whether data is valid
#         if serializer.is_valid():
#             serializer.save()
#             return Response(data=serializer.data)
#         else:
#             return Response(data=serializer.errors)


# ----------------USING MODEL VIEWSET----------------------------------------
        # built in methods for list ,create,retrieve,destroy , partial update functions
        # give only serializer class and queryset

class ProductModelViewset(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Products.objects.all()


class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    








       





    

