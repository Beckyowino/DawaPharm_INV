# Generated by Django 5.0.1 on 2024-03-25 03:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0008_remove_order_status'),
    ]

    operations = [
        migrations.DeleteModel(
            name='SalesInvoice',
        ),
    ]
