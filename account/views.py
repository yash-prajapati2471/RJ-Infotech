from django.shortcuts import render,redirect
from .forms import RegisterForm
from django.http import HttpResponse
from .models import registration as register
from django.contrib.auth import authenticate
from django.contrib.auth import login as user_login
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
            return redirect('index')
        
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
            user_login(request,user)
            return redirect('index')

    return render(request,'account/login.html')