from django.shortcuts import render
from store.models import *
# Create your views here.

def store(request,category_slug=None):

    if category_slug != None:
        pro = product.objects.filter(Category__slug=category_slug,is_active=True)
    
    else:
        pro = product.objects.filter(is_active=True)
        
    return render(request,'store/products.html',{'product':pro})