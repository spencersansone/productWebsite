from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    title = models.CharField(max_length=100)
    product_price = models.FloatField()
    shipping_price = models.FloatField()
    description = models.TextField(max_length=10000)

class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    
    def __str__(self):
        return "{}: {} {}".format(
            self.user.username,
            self.first_name,
            self.last_name)

class SignUpAttempt(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    verification_code = models.CharField(max_length=100)
    verification_code_email_sent = models.BooleanField()

# Create your models here.
