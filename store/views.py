from django.shortcuts import render
from store.models import *
# Create your views here.

def store(request):
    pro = product.objects.all()
    return render(request,'store/products.html',{'product':pro})