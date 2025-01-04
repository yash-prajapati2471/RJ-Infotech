from django.shortcuts import render,redirect
from store.models import product
from django.http import HttpResponse
from carts.models import *

# Create your views here.

def _cart_id(request):
    cart = request.session.session_key
    if cart is None:
        cart = request.session.create()
    return cart


def add_to_cart(request,product_id):
    pro = product.objects.get(id=product_id)

    try:
        cart = Cart.objects.get(session_id=_cart_id(request))
    except:
        cart = Cart.objects.create(session_id=_cart_id(request))

    try:
        cart_products = CartItem.objects.get(product=pro,cart=cart)
        cart_products.quantity += 1
        cart_products.save()
    except CartItem.DoesNotExist:
        CartItem.objects.create(
            product=pro,
            cart=cart,
            quantity=1
        )
    return redirect('cart')


def cart(request):

    try:
        cart = Cart.objects.get(session_id=_cart_id)
        cart_item = CartItem.objects.filter(cart=cart)
    except Cart.DoesNotExist:
        cart_item = []

    context = {
        'cart_items':cart_item,
    }

    return render(request,'store/cart.html',context)

