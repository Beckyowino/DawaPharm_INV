from django.contrib import admin
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
import openpyxl, datetime


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
    list_display = ("product", "created_by", "order_quantity", "date", "client")
    list_filter = ["date", "product", "client"]
    search_fields = ["product"]
    actions = ["download_report"]

    @admin.action(description="Download report required")
    def download_report(self, request, queryset):
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="salesreport.xlsx"'

        workbook = openpyxl.Workbook()
        workbook.iso_dates = True
        worksheet = workbook.active
        worksheet.title = 'Dawa Pharmacy Sales Report'

        # Write header row
        header = ['Product', 'Created_by', 'Order quantity', 'Date', "Client"]
        for col_num, column_title in enumerate(header, 1):
            cell = worksheet.cell(row=1, column=col_num)
            cell.value = column_title

        queryset = queryset.values_list("product__name", "created_by__username", "order_quantity", "date", "client")
        row_num = 2
        
        for row in queryset:
            for col_num, cell_value in enumerate(row, 1):
                if col_num == 4:
                    cell_value = cell_value.replace(tzinfo=None)
                    cell_value = cell_value.strftime("%b %d, %Y, %I:%M:%p")
                cell = worksheet.cell(row=row_num, column=col_num)
                cell.value = cell_value

            row_num += 1
                
        workbook.save(response)
        return response

class UserProfileAdmin(admin.ModelAdmin):
    model = UserProfile
    list_display = ("user", "physical_address", "mobile", "picture")
    # list_filter = ["user__username"]
    search_fields = ["user__username"]

admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(UserProfile, UserProfileAdmin) 
admin.site.register(SalesInvoice)
