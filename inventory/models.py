from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.core.exceptions import ValidationError

CATEGORY = (
    ("Supplements", "Supplements"),
    ("Vitamins", "Vitamins"),
    ("Diet and nutrition", "Diet and nutrition"),
    ("Tea and coffee", "Tea and coffee")
)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    physical_address = models.CharField(max_length=40, null=True)
    mobile = models.CharField(max_length=12, null=True)
    picture = models.ImageField(default="avatar.jpg", upload_to="Pictures")

    def __str__(self) -> str:
        return self.user.username

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

class Product(models.Model):
    name = models.CharField(max_length=100, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY, null=True)
    quantity = models.PositiveIntegerField(null=True)
    description = models.CharField(max_length=200, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    reorder_date = models.DateTimeField(null=True, blank=True)  
    def __str__(self) -> str:
        return self.name
    
    def stock_total_value(self):
        return self.quantity * self.price
    
    def clean(self):
        if self.price <= 0:
                raise ValidationError("Price must be greater than zero.")
        if self.quantity <= 0:
                raise ValidationError("Quantity must be greater than zero.")

    def save(self, *args, **kwargs):
            self.full_clean()
            super().save(*args, **kwargs)
class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    order_quantity = models.PositiveIntegerField(null=True)
    date = models.DateTimeField(auto_now_add=True)
    client = models.CharField(max_length=60)

    def __str__(self) -> str:
        return f"{self.product} ordered quantity {self.order_quantity}"

    def get_total(self):
        return self.order_quantity * self.product.price
    
