from django.shortcuts import render
from store.models import *

def index(request):

    pro = product.objects.all()

    context = {
        'product':pro
    }

    return render(request,'index.html',context)

