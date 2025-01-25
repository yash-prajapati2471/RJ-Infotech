from django.shortcuts import render,redirect

from orders.models import Order, OrderProduct, Payment
from .forms import *
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
from django.contrib.auth.hashers import make_password
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
    messages.success(request,"You have logout successfully.")
    return redirect('login')

def forget_password(request):
    if request.method == "POST":
        email = request.POST.get('email')

        try:
            user = register.objects.get(email=email)
            
            email_subject = "Reset Your Password"
            current_side = get_current_site(request)

            context = {
                'user':user,
                'domain':current_side,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            }
            message = render_to_string('account/password_reset_email.html',context)
            send_email = EmailMessage(email_subject,message,to=[email])
            messages.success(request, "A reset link has been sent to your email.")
            send_email.send()

        except:
            pass

        return redirect(f'/account/newpassword/?command=password_reset_email&email='+email)

    return render(request,'account/forget_password.html')

def newpassword(request):

    if request.method == "POST":
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password==confirm_password:
            user_email = request.session.get('uid')
            user = register.objects.get(email=user_email)
            user.password = make_password(new_password)
            user.save()
            del request.session['uid']
            messages.success(request, "Your password has been reset successfully.")
            return redirect('login')

        else:
            pass
            
    return render(request,'account/newpassword.html')


def password_reset_email(request,uid64,token):
    try:
        userid = urlsafe_base64_decode(uid64).decode()
        user = register._default_manager.get(id=userid)
        if default_token_generator.check_token(user,token):
            request.session['uid'] = user.email
            return redirect('newpassword')
    except:
        pass

    return redirect('forget_password')

@login_required(login_url='login')
def UserDashboard(request):

    user = request.user
    user_profile,created = UserProfile.objects.get_or_create(user=user)

    account_form = AccountForm(instance=user)
    profile_form  = ProfileForm(instance=user_profile)

    if request.method == "POST":
        account_form = AccountForm(request.POST,instance=user)
        profile_form = ProfileForm(request.POST,request.FILES,instance=user_profile)

        if account_form.is_valid() and profile_form.is_valid():
            account_form.save()
            profile_form.save()
            messages.success(request,"Profile updated successfully!")
            return redirect('index')
    
    context = {
        'account_form':account_form,
        'profile_form':profile_form,
    }

    return render(request,'account/user_dashboard.html',context)

@login_required(login_url='login')
def UserOrders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    context = {
        'orders':orders,
    }
    return render(request,'account/UserOrders.html',context)

@login_required(login_url='login')
def UserOrderDetails(request,ordeid):
    other_details = Order.objects.get(id=ordeid)

    orderdetails = OrderProduct.objects.filter(order=other_details) 

    payment_details = Payment.objects.get(payment_id=other_details.payment)

    context = {
        'other_details':other_details,
        'orderdetails':orderdetails,
        'payment_details':payment_details
    }
    return render(request,'account/UserOrderDetails.html',context)
