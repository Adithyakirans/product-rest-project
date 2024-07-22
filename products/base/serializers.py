from rest_framework import serializers
from . models import Products

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

