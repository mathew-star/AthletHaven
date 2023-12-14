
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
