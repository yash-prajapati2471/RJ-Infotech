from django.db import models
from store.models import *
# Create your models here.

class Cart(models.Model):
    cart_id = models.CharField(max_length=255,null=True,blank=True)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cart_id

class CartItem(models.Model):
    product = models.ForeignKey(product,on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def sub_total(self):
        return self.product.product_price * self.quantity
    
    def __str__(self):
        return self.product.product_name
