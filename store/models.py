from django.db import models
from category.models import *
from django.urls import reverse
# Create your models here.

class product(models.Model):
    product_name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=255)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    product_detail = models.CharField(max_length=200)
    product_price = models.IntegerField()
    product_hideprice = models.IntegerField()
    product_stock = models.IntegerField()
    is_active = models.BooleanField(default=True)
    product_image = models.ImageField(upload_to='product_image/')
    creates_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product_name
    
    def get_url(self):
        return reverse('product_detail',args=[self.category.slug,self.slug])