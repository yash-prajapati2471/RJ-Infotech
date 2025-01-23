from django.shortcuts import render,redirect
from .forms import RegisterForm
from carts.models import *
from carts.views import _cart_id
from django.http import HttpResponse
from django.core.mail import EmailMessage       
from .models import registration as register
from django.contrib.auth import authenticate
from django.contrib.auth import login as user_login
from django.contrib.auth import logout as log_out
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib import messages
from django.contrib.auth.decorators import login_required 
# Create your views here.

def registration(request):

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            firstname = form.cleaned_data['firstname']
            lastname = form.cleaned_data['lastname']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            password = form.cleaned_data['password']
            con_password = form.cleaned_data['con_password']

            username = email.split("@")[0]

            user = register.objects.create_user(firstname=firstname,lastname=lastname,email=email,phone=phone,username=username,password=password)
            user.save()
            messages.success(request,"You have Register Success,please cheak out your email")

            

            try:
                email_subject = "Please Active your Email"
                current_side = get_current_site(request)

                context = {
                    'user':user,
                    'domain':current_side,
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                    'token':default_token_generator.make_token(user),
                }
                message = render_to_string('account/verification.html',context)
                send_email = EmailMessage(email_subject,message,to=[email])
                send_email.send()

            except:
                pass

            return redirect(f'/account/login/?command=verification&email='+email)

        else:
            messages.error(request,"User is already register")
            # return redirect('/account/registration/?&email='+email+'&uid='+context.uid)
            return redirect('registration')           
            
        
    else:
        form = RegisterForm()

    context = {
        'form':form
    }

    return render(request,'account/registration.html',context)

def login(request):

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request,username=username,password=password)

        if user is not None:

            try:
                # Merge session cart items into user's cart
                session_cart_id = _cart_id(request)
                session_cart_items = CartItem.objects.filter(cart__cart_id=session_cart_id)
                user_cart_items = CartItem.objects.filter(user=user)

                for session_item in session_cart_items:
                    matching_user_items = user_cart_items.filter(
                        product=session_item.product
                    ).prefetch_related('variation')

                    found_match = False
                    for user_item in matching_user_items:
                        if set(user_item.variation.all()) == set(session_item.variation.all()):
                            user_item.quantity += session_item.quantity
                            user_item.save()
                            found_match = True
                            break

                    if not found_match:
                        session_item.user = user
                        session_item.cart = None  # Detach from session cart
                        session_item.save()

                # Delete the session cart after merging
                session_cart_items.delete()
            except:
                pass

            user_login(request,user)
            next_url = request.GET.get('next','index')
            messages.success(request,"You have login success")
            return redirect(next_url)
        else:
            messages.success(request,"Wrong Email And Password.")
            return redirect('login')

    return render(request,'account/login.html')

def verification(request,uid64,token):
    try:
        userid = urlsafe_base64_decode(uid64).decode()
        user = register._default_manager.get(id=userid)
        tokens = default_token_generator.check_token(user,token)
    except:
        user = None

    if user is not None and tokens:
        user.is_active = True
        user.save()
        return redirect('login')
    else:
        return redirect('registration')
    

def logout(request):
    log_out(request)
    return redirect('login')
