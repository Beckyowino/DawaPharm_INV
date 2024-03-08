from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings


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
    expiry_date = models.DateField(default=timezone.now, null=True)
    price= models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self) -> str:
        return self.name
    
    @property
    def is_expired(self):
        return self.expiry_date < date.today()
    
    def send_expiry_notification(self):
        if self.is_expired:
                    pharmacist = User.objects.filter(groups__name__iexact='Pharmacist').first()
                    subject = f"PRODUCT '{Order.product.name}' HAS EXPIRED"
                    message = f"Product '{Order.product.name}' expiry date is today."

                    send_mail(
                        subject=subject,
                        message=message,
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[pharmacist.email],
                        fail_silently=False,

                    )

class Order(models.Model):
    STATUS_CHOICES = (
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    created_by = models.ForeignKey(User, models.CASCADE, null=True)
    order_quantity = models.PositiveIntegerField(null=True)
    date = models.DateTimeField(auto_now_add=True)
    client = models.CharField(max_length=60)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='COMPLETED')

    def __str__(self) -> str:
        return f"{self.product} ordered quantity {self.order_quantity}"

    def get_total(self):
        return self.order_quantity * self.product.price
    
class SalesInvoice(models.Model):
    invoice_no = models.CharField(max_length=100, unique=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.invoice_no
