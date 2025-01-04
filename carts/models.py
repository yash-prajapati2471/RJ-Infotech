from django.db import models

# Create your models here.

class Cart(models.Model):
    session_id = models.CharField(max_length=255,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.session_id

class CartItem(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    product = models.CharField(max_length=255)
    quantity = models.IntegerField()

    def __str__(self):
        return self.product
