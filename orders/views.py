from django.shortcuts import render
from orders.models import *
from carts.models import *
from datetime import date
from django.views.decorators.csrf import csrf_exempt
import razorpay
import json
# Create your views here.

# @csrf_exempt
# def payment(request):
#     data = json.load(request.body)

#     payment_id = ["razorpay_payment_id"]

#     order = Order.objects.get(user=request.user,is_ordered=False,order_number=data['Order'])

def orderproduct(request):
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
            "recipt":"order_number",
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