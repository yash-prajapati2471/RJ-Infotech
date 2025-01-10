from django.shortcuts import render,redirect
from store.models import product
from django.http import HttpResponse
from carts.models import *
from store.models import *

# Create your views here.

def _cart_id(request):
    cart = request.session.session_key
    if cart is None:
        cart = request.session.create()
    return cart


def add_to_cart(request,product_id):
    pro = product.objects.get(id=product_id)


    if request.method == "POST":
        # for item in request.POST:
        #     key = item
        #     value = request.POST[item]
        #     print(value)
        selected_color = request.POST.get('color')
        selected_size = request.POST.get('size')


        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except:
            cart = Cart.objects.create(cart_id=_cart_id(request))

        try:
            cart_products = CartItem.objects.get(product=pro,cart=cart,color=selected_color,size=selected_size)
            cart_products.quantity += 1
            cart_products.save()
        except:
            cart_products = CartItem.objects.create(
                product=pro,
                cart=cart,
                color=selected_color,
                size=selected_size,
                quantity=1
            )
    return redirect('cart')


def cart(request):
    total = 0

    cart_items = CartItem.objects.filter(cart__cart_id=_cart_id(request))

    for i in cart_items:
        total += (i.product.product_price * i.quantity)

    text = (2*total)/100 

    grand_total = text + total

    context = {
        'cart_items':cart_items,
        'total':total,
        'text':text,
        'grand_total':grand_total
    }

    return render(request,'store/cart.html',context)

def decrease(request,product_id):
    pro = product.objects.get(id=product_id)

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=pro,cart=cart)

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()

        else:
            cart_item.delete()
            
    except CartItem.DoesNotExist:
        pass

    return redirect('cart')

