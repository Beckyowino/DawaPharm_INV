# inventory/urls.py
from django.urls import path
from inventory import views
from django.contrib.auth import views as auth_views

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
    path('generate_sales_report/', views.generate_sales_report, name='generate_sales_report'),
    path('logout/', auth_views.LogoutView.as_view(next_page="home"), name="logout"),
]

