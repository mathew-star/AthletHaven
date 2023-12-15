
from django.db import models
from accounts.models import CustomUser
class BlockedUser(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='blocked_user')

    def __str__(self):
        return self.user.email


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='category/',blank=True)
    is_listed = models.BooleanField(default=True)

    def __str__(self):
        return self.name



    
class Products(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_listed = models.BooleanField(default=True)
    # New fields
    RATING_CHOICES = [
        (1, '4.1'),
        (2, '4.2'),
        (3, '4.3'),
        (4, '4.4'),
        (5, '5'),
    ]
    rating = models.IntegerField(choices=RATING_CHOICES)
    
    STAR_CHOICES = [
        (1, '1 star'),
        (2, '2 stars'),
        (3, '3 stars'),
        (4, '4 stars'),
        (5, '5 stars'),
    ]
    star = models.IntegerField(choices=STAR_CHOICES)

    def __str__(self):
        return self.name

class ProductImages(models.Model):
    image= models.ImageField(upload_to='product_images/')
    product = models.ForeignKey(Products, on_delete=models.CASCADE,related_name='image')
