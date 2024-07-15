from django.db import models

# Create your models here.

class Products(models.Model):
    name = models.CharField(max_length=150)
    price = models.PositiveIntegerField()
    description = models.CharField(max_length=150)
    category = models.CharField(max_length=150)
    image = models.ImageField(null=True)

    def __str__(self):
        self.name

