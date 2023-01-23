from django.shortcuts import render,redirect
from .forms import *
from django.core.mail import send_mail
from emailsend.settings import EMAIL_HOST_USER
import uuid
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate
from django.http import HttpResponse
# Create your views here.
def regis(request):
    a=register()
    return render(request,'abc.html',{'form':a}) #a is passed as context to form key

def email_send(request):
    a=ContactusForm()
    if request.method=='POST':
        sub=ContactusForm(request.POST)
        if sub.is_valid():
            nm=sub.cleaned_data['Name']
            em=sub.cleaned_data['Email']
            ms=sub.cleaned_data['Message']
            send_mail(str(nm)+"||"+"TCS",ms,EMAIL_HOST_USER,[em])
            return render(request,'success.html')
    return render(request,'email.html',{'form':a})

def reg(request):
    if request.method=='POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        if User.objects.filter(username=username).first():
            messages.success(request,'username already taken')
            return redirect(reg) #same pageil refresh cheyth nikkan vendi ta username already taken aayathond
        if User.objects.filter(email=email).first():
            messages.success(request,'email already exist') #nth msg aano display page il dispaly cheyadathe
            return redirect(reg)
        # password ne set_password aayite seperate save cheyum secure aakan vndi
        # username and email are directly saved to user_obj and stored in User model
        #2 if um work cheyunilenkil

        user_obj=User(username=username,email=email)
        user_obj.set_password(password)
        user_obj.save()

        auth_token=str(uuid.uuid4()) #uuid-universely unique identifier

        profile_obj=profile.objects.create(user=user_obj,auth_token=auth_token)
        profile_obj.save()
        #ithrem ok aanenkil send_mail_regis nammal create cheyanam
        send_mail_regis(email,auth_token) #mail sending function
        return render(request,'success.html')
    return render(request,'register.html')

def send_mail_regis(email,auth_token):
    subject="your account has been verified"
    message=f'paste the link to verify your account  http://127.0.0.1:8000/emailapp/verify/{auth_token}' #f string formatter
    email_from=EMAIL_HOST_USER #already created in setings  #from
    recipient=[email] #to
    send_mail(subject,message,email_from,recipient)

def verify(request,auth_token): #123
    profile_obj=profile.objects.filter(auth_token=auth_token).first()
    if profile_obj: #if true
        if profile_obj.is_verified: #if profile object is false
            messages.success(request,'your account is already verified')
            return redirect(login)
        profile_obj.is_verified=True
        profile_obj.save()
        messages.success(request,'your account has been verified')
        return redirect(login) #login function (login)
    else:
        messages.success(request,'user not found')
        return redirect(login)

def login(request):
    if request.method=="POST":

        username=request.POST.get('username')
        password=request.POST.get('password')
        user_obj=User.objects.filter(username=username).first()
        #user_obj=merin
        if user_obj is None: #if user doesn't exist
            messages.success(request,'user not found')
            return redirect(login)#login
        profile_obj=profile.objects.filter(user=user_obj).first()
        if not profile_obj.is_verified: #if not profile is false
            messages.success(request,'profile not verified check your mail')
            return redirect(login)
        user=authenticate(username=username,password=password)
        if user is None:
            messages.success(request,'wrong password or username')
            return redirect(login)
        return HttpResponse("success")
    return render(request,'login.html')