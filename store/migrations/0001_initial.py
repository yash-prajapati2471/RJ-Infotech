# Generated by Django 5.1.4 on 2025-01-01 17:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('category', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=200)),
                ('slug', models.SlugField(max_length=200)),
                ('product_detail', models.CharField(max_length=200)),
                ('product_price', models.IntegerField()),
                ('product_stock', models.IntegerField()),
                ('is_active', models.BooleanField(default=True)),
                ('product_image', models.ImageField(upload_to='product_image/')),
                ('creates_at', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='category.category')),
            ],
        ),
    ]