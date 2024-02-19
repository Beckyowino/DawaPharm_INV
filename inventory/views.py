"""from django.shortcuts import render
from django.views.generic import TemplateView

class Index(TemplateView):
    template_name = 'inventory/index2.html'"""

# inventory/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from inventory.forms import UserRegistry, ProductForm, OrderForm
from inventory.models import Product, Order

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
    context = {"title": "Products", "products": products, "form": form}
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

@login_required
def sales_report(request):
    total_sales = sum(order.total for order in orders)  # Calculate total sales
    #completed_orders = Order.objects.filter(status='completed') Get only completed orders
    #cancelled_orders = Order.objects.filter(status='cancelled')  Get only cancelled orders
    def cancelled_orders():
    # ... (logic to filter cancelled orders)
        cancelled_orders = Order.objects.filter(status='cancelled')  # Assuming this retrieves cancelled orders
        return cancelled_orders
    
    def completed_orders():
    # ... (logic to filter cancelled orders)
        completed_orders = Order.objects.filter(status='completed')  # Assuming this retrieves cancelled orders
        return completed_orders

    context = {
        "title": "Sales Report",
        "completed_orders": completed_orders,
        "cancelled_orders": cancelled_orders,
        "total_sales": total_sales,
    }
    return render(request, "inventory/sales_report.html", context)

def search(request):
    if request.method == 'GET':
        query = request.GET.get('query')
        if query:  # Check if a query was submitted
            results = Product.objects.filter(name__icontains=query)  # Adjust filtering criteria
            context = {'search_query': query, 'results': results}
            return render(request, 'search_results.html', context)
    else:
        return render(request, 'index.html')  # Redirect to homepage or appropriate page
