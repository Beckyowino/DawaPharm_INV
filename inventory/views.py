# inventory/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from inventory.forms import UserRegistry, ProductForm, OrderForm
from inventory.models import Product, Order
from django.db.models import Sum

@login_required
def index(request):
    orders_user = Order.objects.all()
    users = User.objects.all()[:2]
    orders_adm = Order.objects.all()[:2]
    products = Product.objects.all()[:2]
    reg_users = len(User.objects.all())
    all_prods = len(Product.objects.all())
    all_orders = len(Order.objects.all())
    context = {
        "title": "Home",
        "orders": orders_user,
        "orders_adm": orders_adm,
        "users": users,
        "products": products,
        "count_users": reg_users,
        "count_products": all_prods,
        "count_orders": all_orders,
    }
    return render(request, "inventory/index.html", context)

def index2(request):
    context = {}
    return render(request, "inventory/index2.html", context)

def about(request):
    context = {}
    return render(request, "inventory/about.html", context)

def contact(request):
    context = {}
    return render(request, "inventory/contact.html", context)

@login_required
def products(request):
    products = Product.objects.all()
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("products")
    else:
        form = ProductForm()
    context = {"title": "Products", "products": products, "form": form, "prices": {product.name: product.price for product in products}
            }
    return render(request, "inventory/products.html", context)

@login_required
def orders(request):
    orders = Order.objects.all()
    print([i for i in request])
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.created_by = request.user
            instance.save()
            return redirect("orders")
    else:
        form = OrderForm()
    context = {"title": "Orders", "orders": orders, "form": form}
    return render(request, "inventory/orders.html", context)

@login_required
def users(request):
    users = User.objects.all()
    context = {"title": "Users", "users": users}
    return render(request, "inventory/users.html", context)

@login_required
def user(request):
    context = {"profile": "User Profile"}
    return render(request, "inventory/user.html", context)

def register(request):
    if request.method == "POST":
        form = UserRegistry(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserRegistry()
    context = {"register": "Register", "form": form}
    return render(request, "inventory/register.html", context)

def completed_orders():
    return Order.objects.filter(status='completed')

def cancelled_orders():
    return Order.objects.filter(status='cancelled')

@login_required
def sales_report(request):
    total_sales = sum(order.total for order in Order.objects.all())  # Calculate total sales
    orders_by_date = Order.objects.order_by('date').values('date').annotate(total=Sum('total'))  # Group orders by date and calculate total sales for each date
    completed_orders_queryset = completed_orders()  # Get completed orders
    cancelled_orders_queryset = cancelled_orders()  # Get cancelled orders
    prices = {product.name: product.price for product in Product.objects.all()}

    context = {
        "title": "Sales Report",
        "orders_by_date": orders_by_date,
        "completed_orders": completed_orders_queryset,
        "cancelled_orders": cancelled_orders_queryset,
        "total_sales": total_sales,
        "prices": prices,

    }
    return render(request, "inventory/sales_report.html", context)

@login_required
def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("products")
    else:
        form = ProductForm()
    context = {"title": "Create Product", "form": form}
    return render(request, "inventory/product_form.html", context)

@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return redirect("products")