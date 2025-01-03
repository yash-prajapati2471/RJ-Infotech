from django.shortcuts import render
from store.models import *
# Create your views here.

def store(request,category_slug=None):

    if category_slug != None:
        pro = product.objects.filter(category__slug=category_slug,is_active=True)
    
    else:
        pro = product.objects.filter(is_active=True)
        
    return render(request,'store/products.html',{'product':pro})


def product_detail(request,category_slug,product_slug):

    single_product = product.objects.get(category__slug=category_slug,slug=product_slug)

    context = {
        'single_product':single_product,
    }

    return render(request,'store/product_detail.html',context)