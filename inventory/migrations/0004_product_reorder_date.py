# Generated by Django 5.0.1 on 2024-03-13 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='reorder_date',
            field=models.DateTimeField(null=True),
        ),
    ]
