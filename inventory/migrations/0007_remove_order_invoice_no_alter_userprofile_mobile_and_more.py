# Generated by Django 5.0.1 on 2024-03-17 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0006_rename_medicine_salesinvoice_product_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='invoice_no',
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='mobile',
            field=models.CharField(max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='physical_address',
            field=models.CharField(max_length=40, null=True),
        ),
    ]