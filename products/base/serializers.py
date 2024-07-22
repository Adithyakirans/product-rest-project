from rest_framework import serializers
from . models import Products
from django.contrib.auth.models import User

# class ProductSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(max_length=150)
#     price = serializers.IntegerField()
#     description = serializers.CharField(max_length=150)
#     category = serializers.CharField(max_length=150)
#     image =serializers.ImageField()



# Using modelserializer

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Products
        fields = ['id','name','price','description','category']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name','last_name','email','username','password']
