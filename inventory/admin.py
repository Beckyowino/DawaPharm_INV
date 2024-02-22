from django.contrib import admin
from django.conf import settings
from django.core.mail import send_mail
from inventory.models import Order

# Register your models here.
# inventory/admin.py
from inventory.models import Product, Order, UserProfile, SalesInvoice

admin.site.site_header = "Inventory Admin"

class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ("name", "category", "quantity", "price")
    list_filter = ["category"]
    search_fields = ["name"]
    list_editable = ["quantity", "price"]
    actions = ["reorder_product_from_supplier"]

    @admin.action(description="Reorder products that are below minimum stock level")
    def reorder_product_from_supplier(self, request, queryset):
        message = ''
        for product in queryset:
            if product.quantity <= settings.MIN_STOCK_QUANTITY:
                reorder_quantity = 10 - product.quantity
                print(f"Reordering {reorder_quantity} units of {product.name}")
                product.quantity += reorder_quantity
                product.save()
                message += f"{product.name}: {reorder_quantity}.\n"

        message = "Please supply me with the requested quantities for the following products:\n" + message
        send_mail(
            subject="REQUEST FOR PRODUCTS SUPPLY",
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.EMAIL_SUPPLIER],
            fail_silently=False,
        )

class OrderAdmin(admin.ModelAdmin):
    model = Order
    list_display = ("product", "created_by", "order_quantity", "date")
    list_filter = ["date"]
    search_fields = ["product"]


class UserProfileAdmin(admin.ModelAdmin):
    model = UserProfile
    list_display = ("user", "physical_address", "mobile", "picture")
    # list_filter = ["user__username"]
    search_fields = ["user__username"]


admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(SalesInvoice)
