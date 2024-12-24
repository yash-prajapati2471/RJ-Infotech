from django.shortcuts import render,redirect
from .forms import RegisterForm
from django.http import HttpResponse
from .models import registration as register
# Create your views here.

def registration(request):

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            firstname = form.cleaned_data['firstname']
            lastname = form.cleaned_data['lastname']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            con_password = form.cleaned_data['con_password']
            username = email.split("@")[0]

            user = register.objects.create_user(firstname=firstname,lastname=lastname,email=email,username=username,password=password)
            user.save()
            return redirect('index')
        
    else:
        form = RegisterForm()

    context = {
        'form':form
    }

    return render(request,'account/registration.html',context)

def login(request):
    return render(request,'account/login.html')