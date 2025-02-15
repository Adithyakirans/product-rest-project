from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Products,Cart,Reviews
from .serializers import ProductSerializer,UserSerializer,CartSerializer,ReviewSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from django.contrib.auth.models import User
from rest_framework import authentication,permissions
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
    # adding authentication and permissions
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]


# custom method for add to cart function
    @action(methods=['POST'],detail=True)
    def addto_cart(self,request,*args,**kwargs):
        # get the product id
        id = kwargs.get('pk')
        product = Products.objects.get(id=id)
        user = request.user
        # create or add details to cart
        user.cart_set.create(product=product)
        return Response(data={'message':'product added to cart'})
    
# custom method for adding review
    # localhost:8000/base/products/id/add_review
    @action(methods=['POST'],detail=True)
    def add_review(self,request,*args,**kwargs):
        user = request.user
        id = kwargs.get('pk')
        product = Products.objects.get(id=id)
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user,product=product)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        
# getting reviews
        # localhost:8000/base/products/id/review
    @action(methods=['GET'],detail=True)
    def review(self,request,*args,**kwargs):
        # get review of given id
        # id =kwargs.get('pk')
        # product = Products.objects.get(id=id)

# when user already passed the id theres built in method to retrieve product details
        product = self.get_object()
        reviews = product.reviews_set.all()
        serializer = ReviewSerializer(reviews,many=True)
        return Response(data=serializer.data)

    

class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


# listing cart details of the user

class CartView(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    queryset = Cart.objects.all()
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

# here we are over riding list function of in model viewset because list function list out all data in cart , as we need data of a specific logined user

    def list(self,request,*args,**kwargs):
        # list out data inside the cart of the particular user
        qs = request.user.cart_set.all()
        serializer = CartSerializer(qs,many=True)
        return Response(data=serializer.data)
# we are overriding get queryset of generic api view
    # def get_queryset(self):
    #     return self.request.user.cart_set.all() OR
    #     return self.request.user.cart_set.filter(is_active=True) OR
    #     return Cart.objects.filter(user=self.request.user)



# deleting a review using api view
class Delete_review(APIView):
        def delete(self,request,*args,**kwargs):
            id = kwargs.get('pk')
            Reviews.objects.get(id=id).delete()
            return Response(data={"message":"review deleted"})









       





    

