from django.db import models
from email.policy import default
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=200, blank=True)
# Create your models here.

GENDER = (
    ("M", "Male"),
    ("F", "Female"),
    ("O", "Other"),
)

class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fname = models.CharField(max_length=20)
    lname = models.CharField(max_length=20)
    sex = models.CharField(max_length=2, choices=GENDER)
    email = models.EmailField(max_length=100)
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=200, blank=True)

    def _str_(self):
        return self.name

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fname = models.CharField(max_length=20)
    lname = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=200, blank=True)

    def _str_(self):
        return self.name

class Medicine(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()

    def _str_(self):
        return self.name

class SalesInvoice(models.Model):
    invoice_no = models.CharField(max_length=100, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.invoice_no

class Supplier(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=100)

    def _str_(self):
        return self.name 
