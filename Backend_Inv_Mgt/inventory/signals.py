from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from inventory.models import Order
from inventory.models import User


@receiver(post_save, sender=Order)
def my_handler(sender, instance, **kwargs):
    # order = kwargs['instance']
    order = instance
    
    # Update the stock quantity
    order.product.quantity = order.product.quantity - order.order_quantity
    order.product.save()

    # Notify phamarcist
    if order.product.quantity <= settings.MIN_STOCK_QUANTITY:
        pharmacist = User.objects.filter(groups__name__iexact='PharmAcist').first()
        subject = f"PRODUCT '{order.product.name}' STOCK IS LOW"
        message = f"Product '{order.product.name}' is running low. Current quantity is {order.product.quantity}."

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[pharmacist.email],
            fail_silently=False,

        )



