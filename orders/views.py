from django.shortcuts import render
from django.http import JsonResponse
from orders.models import *
from carts.models import *
from datetime import date
from django.views.decorators.csrf import csrf_exempt
import razorpay
import json
# Create your views here.

@csrf_exempt
def payment(request):
    data = json.loads(request.body)
    print(data['Order'])
    payment_id = data["razorpay_payment_id"]

    order = Order.objects.get(user=request.user,is_ordered=False,order_number=data['Order'])
    print(order)

    try:
        payment = Payment(
            user=request.user,
            payment_id=payment_id,
            payment_method="Razorpay",
            amount_paid=data['Amount'],
            status=True
        )
        payment.save()

        order.payment = payment
        order.is_ordered = True
        order.save()

        cart_item = CartItem.objects.filter(user=request.user)

        for item in cart_item:
            parchsedproduct = OrderProduct()
            parchsedproduct.order = order
            parchsedproduct.user = request.user
            parchsedproduct.payment = payment
            parchsedproduct.product = item.product
            parchsedproduct.quantity = item.quantity
            parchsedproduct.product_price = item.product.product_price
            parchsedproduct.is_ordedred = True

            parchsedproduct.save()

            parchsedproduct.variations.set(item.variation.all())
            parchsedproduct.save()

            product = item.product
            if product.product_stock >= item.quantity:
                product.product_stock -= item.quantity
                product.save()

        cart_item.delete()

        ds = {"success":True}
        return JsonResponse(ds)

    except:
        pass

def place_order(request):
    total = 0

    cart_items = CartItem.objects.filter(user=request.user)

    for i in cart_items:
        total += (i.product.product_price * i.quantity)

    text = (2*total)/100 

    grand_total = text + total

    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        address_line_1 = request.POST['address_line_1']
        address_line_2 = request.POST['address_line_2']
        country = request.POST['country']
        state = request.POST['state']
        city = request.POST['city']
        order_note = request.POST['order_note']

        new_order = Order.objects.create(
            user=request.user,
            first_name=first_name,
            last_name=last_name,
            address_line_1=address_line_1,
            address_line_2=address_line_2,
            country=country,
            state=state,
            city=city,
            order_note=order_note,
            tax=text,
            total=grand_total,
            ip = request.META.get('REMOTE_ADDR')
        )

        today = date.today()
        formatted_date = today.strftime("%d%m%Y") + str(new_order.id)
        new_order.order_number = formatted_date
        new_order.save() 

        client = razorpay.Client(auth=("rzp_test_susforIvG6nYky","VUQ8dfvBSkVS9Lstz9r1pQ9r"))

        razorpay_client = client.order.create({
            "amount":int(grand_total * 100),
            "currency":"INR",
            "receipt":"order_number",
            "payment_capture":1,
        })

        context = {
            'cart_items':cart_items,
            'text':text,
            'grand_total':grand_total,
            'order':new_order,
            'razorpay_order_id':razorpay_client['id'],
            'key':"rzp_test_susforIvG6nYky",
            'amounts':razorpay_client['amount']
        }

        return render(request,'order/payment.html',context)