"""from django.contrib import admin
from django.urls import path
from .views import Index

urlpatterns = [
    path('admin/', Index.as_view(), name='index'),
]"""

# inventory/urls.py
from django.urls import path
from inventory import views

urlpatterns = [
    path("", views.index2, name="home"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("dash/", views.index, name="dash"),
    path("products/", views.products, name="products"),
    path("orders/", views.orders, name="orders"),
    path("users/", views.users, name="users"),
    path("user/", views.user, name="user"),
    path("register/", views.register, name="register"),
    path("sales_report/", views.sales_report, name="sales_report"),
]

