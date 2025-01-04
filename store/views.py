from django.shortcuts import render,redirect
from store.models import *
from account.models import registration
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

def add_to_cart(request):
    
    product_id = request.GET.get('product_id')
    Product = product.objects.get(id=product_id)
    registration(product_name=Product).save()
    return redirect('/cart/')


