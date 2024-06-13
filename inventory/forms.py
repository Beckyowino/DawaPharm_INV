# inventory/forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from inventory.models import Product, Order
from django.core.exceptions import ValidationError
class UserRegistry(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        ]

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "category", "quantity", "description", "price" ]

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["product", "order_quantity", "client"]
    
    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get("product")
        order_quantity = cleaned_data.get("order_quantity")

        if order_quantity and product:
            # Only do something if both fields are valid so far.
            if order_quantity>product.quantity:
                raise ValidationError(
                    " The order is above the stock level"
                )
            

