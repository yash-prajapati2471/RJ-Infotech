# Generated by Django 5.1.4 on 2025-01-02 04:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_product_product_detail'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='creates_at',
        ),
    ]