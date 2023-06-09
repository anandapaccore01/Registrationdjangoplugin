from django.shortcuts import render,HttpResponse,redirect,HttpResponseRedirect,reverse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib import messages
from django.db.models import Q
from twilio.rest import Client
from django.conf import settings
from datetime import datetime
from .utill import *
from .forms import *

# Create your views here.
def handle_not_found(request,path):
    return HttpResponse('INVALID PAGE')


def homeview(request):
    return render(request, 'base.html')

def Registerview(request):     
    if request.method == 'POST':
        form=RegistrationForm(request.POST)          
        if form.is_valid():
            user = Users.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            username = request.POST['username'],           
            email = request.POST['email'],   
            phone = request.POST['phone'],            
            )
            user.set_password(request.POST['password'])
            user.save()          
            sendemail(user)
            messages.success(request,'User is successfully register, A verification link is sent your email')
            return redirect('register')            
        return render(request, 'registrations.html',{'form':form})       
    else:
        form=RegistrationForm()
        
        return render(request, 'registrations.html',{'form':form})
    
def emailactivate(request, token): 
    try:
        decoded_token = jwt.decode(token,settings.SECRET_KEY,algorithms=["HS256"]) 
        user_id = decoded_token.get("user_id")
        expiry_time = decoded_token.get("expiry")
        print("User ID:", user_id)
        print("Expiry Time:", expiry_time)
        print(token)
        try:
            user=Users.objects.get(id=user_id) 
        except(TypeError, ValueError, OverflowError, user.DoesNotExist):
            user = None
        if user is None:
            return  HttpResponse('User not found')
        user.is_active = True
        user.status = 'Active'
        user.save()
        messages.success(request, 'Successfully, your EMAIL ID is verified. you can login now.')
        return redirect('login')          
    except jwt.DecodeError:
        return HttpResponse("Invalid token")
    # user_id=request.GET.get('user_id','')
    # confirmation_token = request.GET.get('confirmation_token','')
    # timespan = request.GET.get('timespan','')   
    # dt=datetime.now().time()
    # dt=dt.hour*3600+dt.minute*60+dt.second
    # elapsed_time=dt-int(timespan)
    # print(elapsed_time)
    # if elapsed_time > 60:
    #     return HttpResponse('Token is expired. Please request another confirmation email by signing in.')
    # else:
    #     try:
    #         user=Users.objects.get(pk=user_id) 
    #     except(TypeError, ValueError, OverflowError, user.DoesNotExist):
    #         user = None
    #     if user is None:
    #         return  HttpResponse('User not found')
    #     user.is_active = True
    #     user.status = 'Active'
    #     user.save()
    #     messages.success(request, 'Successfully, your EMAIL ID is verified. you can login now.')
    #     return redirect('login')
    return HttpResponse(token)

def loginview(request):
    if request.method == 'POST':
        username=request.POST.get('username')         
        password = request.POST.get('password')
        try:
            my_user = Users.objects.get(Q(username=username)|Q(email=username))
        except Users.DoesNotExist:
            my_user=None        
        if my_user is not None:
            username = my_user.username
            if my_user.status == 'Active':
                user = authenticate(username=username, password=password)
                if user is not None:                    
                    login(request, user) 
                    #return HttpResponse('user is successfully login')
                    return HttpResponseRedirect('profile/%d'%user.id)
                else:
                    messages.error(request, 'Invalid credentials')
                    return redirect('login')
            else:
                sendemail(my_user)
                messages.error(request, 'your email is not verified, Please check your register EMAIL ID.')
                return redirect('login')       
        else:
           messages.error(request, 'Invalid credentials')
           return redirect('login')
    else:
        return render(request, 'login.html')

def Profileview(request,id):
    user=Users.objects.get(id=id)    
    return render(request, 'profile.html',{'user':user})

def logoutview(request):
    logout(request)
    messages.info(request,'u logout successfully')
    return redirect('login')

def changeemail(request):
    if request.method == 'POST':
        form = ChangeemailForm(request.POST)
        id=request.POST.get('user_id')
        user=Users.objects.get(id=id)
        print(form.is_valid())
        if form.is_valid():
            sendchangeemail(request.POST['email'],user)
            messages.success(request,'A verification link is sent your new email, please verify emailID')
            user.email=request.POST['email']
            user.status = 'Inactive'
            user.save()
            return redirect('logout')
        else:
            return render(request, 'profile.html',{'form':form})
    else:
        form = ChangeemailForm()
        return render(request, 'profile.html',{'form':form})
    
def resetpasswordView(request):
    if request.method == 'POST':        
        form = ResetpasswordemailForm(request.POST)
        if form.is_valid():
            user=Users.objects.get(email=form.cleaned_data.get('email'))            
            token = PasswordResetTokenGenerator().make_token(user)
            print(token)
            send_resetpasswordemail(user,token)
            messages.info(request, 'A reset password link is send to your email')
            return redirect('login')
        else:
            return render(request, 'reset_password.html',{'form':form})
    else:
        return render(request, 'reset_password.html')

def resetpassword(request):
    user_id=request.GET.get('user_id','')
    user = Users.objects.get(pk=user_id)
    token = request.GET.get('token','')
    timespan = request.GET.get('timespan','')   
    dt=datetime.now().time()
    dt=dt.hour*3600+dt.minute*60+dt.second
    elapsed_time=dt-int(timespan)
    print(elapsed_time)
    if elapsed_time > 300:
        return HttpResponse('Token is expired')
    else:
        print(token)
        check = PasswordResetTokenGenerator().check_token(user,token=token)
        print(check)
        if check:
            if request.method=='POST':
                form = ResetpasswordFrom(request.POST)
                if form.is_valid():
                    user.set_password(form.cleaned_data.get('password'))
                    user.save()
                    messages.success(request, 'Your password is changed successfully')
                    return redirect('login')
                else:       
                    return render(request, 'change_password.html',{'form':form})
            else:
                return render(request, 'change_password.html')
        else:
            return HttpResponse(" Invalid user or token")
    

def send_otp(request):
    if request.method=="POST":
        phone=request.POST.get("phone")
        id=request.POST.get('user_id')
        user=Users.objects.get(id=id)
        otp=str(random.randint(1000, 9999))
        user.otp=otp
        user.save()
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        print(phone)
        print(settings.TWILIO_PHONE_NUMBER)
        try:
        # Send the OTP message using Twilio
            message = client.messages.create(
                body=f'Your OTP is: {otp}',
                from_= '+13613444861',
                to=phone
            )
            print(message.sid)
            messages.error(request, ' send OTP sucessfully')
            return redirect('verify_otp')
        except Exception as e:
            
            messages.error(request, 'Failed to send OTP', extra_tags='form1')
            return HttpResponseRedirect('profile/%d'%user.id)
    
    

def verify_otp(request):
    if request.method=="POST":
        otp1=request.POST.get('otp1')
        otp2=request.POST.get('otp2')
        otp3=request.POST.get('otp3')
        otp4=request.POST.get('otp4')
        otp=otp1+otp2+otp3+otp4
        id=request.POST.get('user_id')
        user=Users.objects.get(id=id)
        

        if str(user.otp) == otp:
            user.phone_verify=True
            user.save()
            messages.success(request, 'your phone is successfully verified')
            return HttpResponseRedirect('profile/%d'%user.id)
        else:
            messages.error(request, 'Invalid OTP')
        return render(request, 'profile.html')

    return render(request, 'otp.html')