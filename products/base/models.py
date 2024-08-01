from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator


# Create your models here.

class Products(models.Model):
    name = models.CharField(max_length=150)
    price = models.IntegerField()
    description = models.CharField(max_length=150)
    category = models.CharField(max_length=150)
    image = models.ImageField(null=True,blank=True)
    

    def __str__(self):
        return self.name
    
class Cart(models.Model):
    product = models.ForeignKey(Products,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

class Reviews(models.Model):
    product = models.ForeignKey(Products,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    comments = models.CharField(max_length=150)

    def __str__(self):
        return self.comments


