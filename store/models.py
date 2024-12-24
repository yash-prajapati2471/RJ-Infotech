from django.db import models

# Create your models here.

class product(models.Model):
    product_name = models.CharField(max_length=200)
    product_detail = models.CharField(max_length=200)
    product_price = models.IntegerField()
    product_stock = models.IntegerField()
    product_image = models.ImageField(upload_to='product_image/')

    def __str__(self):
        return self.product_name