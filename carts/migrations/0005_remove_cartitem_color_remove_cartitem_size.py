# Generated by Django 5.1.2 on 2025-01-09 17:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0004_cartitem_color_cartitem_size'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='color',
        ),
        migrations.RemoveField(
            model_name='cartitem',
            name='size',
        ),
    ]
