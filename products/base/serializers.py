from rest_framework import serializers
from . models import Products,Cart,Reviews
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

    # method to overwrite create method inside modelserializer class
        # ie this will hash the password

    def create(self,validated_data):
        return User.objects.create_user(**validated_data)
    
class CartSerializer(serializers.ModelSerializer):
    user = serializers.CharField(read_only=True)
    product = serializers.CharField(read_only=True)
    date = serializers.CharField(read_only=True)

    class Meta:
        model = Cart
        fields = ['user','product','date']
    
class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.CharField(read_only=True)
    product = serializers.CharField(read_only=True)

    class Meta:
        model = Reviews
        fields = '__all__'