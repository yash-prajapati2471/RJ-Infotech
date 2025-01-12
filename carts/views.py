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

    product_variation = []
    if request.method == "POST":
        for item in request.POST:
            key = item
            value = request.POST[key]

            try:
                variation = Veriation.objects.get(Product=pro,variation_category__iexact=key,variation_value__iexact=value)
                product_variation.append(variation)
            except:
                pass


    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))

    is_product_var_exi = CartItem.objects.filter(product=pro,cart=cart)

    if is_product_var_exi:
        cart_items = CartItem.objects.filter(product=pro,cart=cart)
        exi_var_list = []
        id = []

        for item in cart_items:
            existing_variations = item.variation.all()
            exi_var_list.append(list(existing_variations))
            id.append(item.id)

        if product_variation in exi_var_list:
            index = exi_var_list.index(product_variation)
            item_id = id[index]
            item = CartItem.objects.get(product=pro,id=item_id)
            item.quantity += 1 
            item.save()

        else:
            cart_products = CartItem.objects.create(product = pro,cart = cart,quantity = 1)
            if len(product_variation) > 0:
                cart_products.variation.clear()
                cart_products.variation.add(*product_variation)
    else:
        cart_products = CartItem.objects.create(
            product=pro,
            cart=cart,
            quantity=1
        )
        if len(product_variation) > 0:
            cart_products.variation.clear()
            cart_products.variation.add(*product_variation)
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

def decrease(request,product_id,cart_item_id):
    pro = product.objects.get(id=product_id)

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=pro,cart=cart,id=cart_item_id)

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()

        else:
            cart_item.delete()
            
    except CartItem.DoesNotExist:
        pass

    return redirect('cart')

