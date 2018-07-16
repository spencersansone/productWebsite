from django.shortcuts import render, get_object_or_404,redirect
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views import generic
from django.contrib.auth import authenticate, login, logout
from random import randint
from email.mime.text import MIMEText
import smtplib
import re
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q

def sendGmail(info):
    msg = MIMEText(u'{}'.format(info['b']),'html')
    msg['Subject'] = info['s']
    msg['From'] = info['g_sender']
    msg['To'] = info['r_email']
    try:
        print("Attempting to send, please wait...")
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(info['g_sender'], info['g_pass'])
        server.sendmail(info['g_sender'], info['r_email'], msg.as_string())
        server.close()
        print('Email sent!')
    except:
        print('Something went wrong...')

def generateVerificationCode():
    return randint(10001,98765)

def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username.lower(), password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))
                return redirect("main:product_list")
        else:
            x = {}
            x['error_message'] = 'Invalid login'
            x['usernameAttempted'] = username
            return render(request, 'main/login.html', x)
    else:
        if request.user.is_authenticated is True:
            return render(request, 'main/login.html')
        elif request.GET.get('next'):
            return render(request, 'main/login.html', {'error_message': 'You must log in to see this page' })
    return render(request, 'main/login.html')

def logout_user(request):
    logout(request)
    return redirect('main:login_user')
    
def signup(request):
    error_messages = []
    
    first_namePattern = "[A-Za-z]+"
    last_namePattern = "[A-Za-z]+"
    emailPattern = "[^@]+@[^@]+\.[^@]+"
    usernamePattern = "[A-Za-z0-9@.+-_]+"
    passwordPattern = "[\S\s]{8,16}"
        
    if request.method == "POST":
        
        first_name= request.POST.get('first_name').lower().capitalize()
        if not re.compile(first_namePattern).match(first_name):
            error_messages += ["Please enter a valid first name."]
        
        last_name = request.POST.get('last_name').lower().capitalize()
        if not re.compile(last_namePattern).match(last_name):
            error_messages += ["Please enter a valid last name."]
        
        username = request.POST.get('username').lower()
        print(username)
        if not re.compile(usernamePattern).match(username):
            error_messages += ["Please enter a valid username."]
        else:
            try:
                uniqueUserCheck = User.objects.get(username=username)
                error_messages += ["Username already exists, please try a different one."]
            except:
                pass
        
        
        email = request.POST.get('email')
        if not re.compile(emailPattern).match(email):
            error_messages += ["Please enter a valid email."]
        else:
            try:
                uniqueEmailCheck = UserProfile.objects.get(email=email)
                error_messages += ["Email already exists, please try a different one."]
            except:
                pass

        password1 = request.POST.get('password1')
        if not re.compile(passwordPattern).match(password1):
            error_messages += ["Please enter a valid password."]
        password2 = request.POST.get('password2')
        
        if not password2 == password1:
            error_messages += ["Passwords do not match, please try again."]
            
        if len(error_messages) > 0:
            x = {}
            x['first_namePattern'] = first_namePattern
            x['last_namePattern'] = last_namePattern
            x['emailPattern'] = emailPattern
            x['usernamePattern'] = usernamePattern
            x['passwordPattern'] = passwordPattern
            
            x['error_messages'] = error_messages
            
            x['first_nameAttempted'] = first_name
            x['last_nameAttempted'] = last_name
            x['emailAttempted'] = email
            x['usernameAttempted'] = username
            x['passwordAttempted'] = password1
            return render(request, 'main/signupProcess/signupForm.html', x)
        
        attemptObj = SignUpAttempt.objects.create(
            first_name = first_name,
            last_name = last_name,
            email = email,
            username = username,
            password = password1,
            verification_code = generateVerificationCode(),
            verification_code_email_sent = False)
        
        request.session['attempt_id'] = attemptObj.id
        return HttpResponseRedirect(reverse('main:verification_code'))
    else:
        x = {}
        x['first_namePattern'] = first_namePattern
        x['last_namePattern'] = last_namePattern
        x['emailPattern'] = emailPattern
        x['usernamePattern'] = usernamePattern
        x['passwordPattern'] = passwordPattern
        return render(request, 'main/signupProcess/signupForm.html', x)

def verificationCode(request):
    if request.method == "POST":
        verification_code = request.POST.get('verification_code').replace(" ","")
        attempt_id = request.POST.get('attempt_id')
        
        attemptObj = SignUpAttempt.objects.get(id=attempt_id)
        
        if verification_code == attemptObj.verification_code:
            userObj = User.objects.create_user(
                username = attemptObj.username,
                password = attemptObj.password)
            
            UserProfile.objects.create(
                user = userObj,
                first_name = attemptObj.first_name,
                last_name = attemptObj.last_name,
                email = attemptObj.email)
            
            SignUpAttempt.objects.filter(
                Q(username=attemptObj.username) | Q(email=attemptObj.email)
                ).delete()
            
            login(request,userObj)
            
            # return render(request, 'main/profile.html')
            return redirect('main:product_list')
        else:
            x = {}
            x['attempt_id'] = request.session.get('attempt_id')
            x['error_message'] = "Incorrect code, please try again."
            return render(request, 'main/signupProcess/verificationCode.html',x)
        
    else:
        attempt_id = request.session.get('attempt_id')
        attemptObj = SignUpAttempt.objects.get(id=attempt_id)
        
        x = {}
        x['attempt_id'] = attempt_id
        
        serverEmailObj = User.objects.get(username="SERVEREMAIL")
        
        info = {}
        info['g_sender'] = serverEmailObj.email
        info['g_pass'] = serverEmailObj.first_name
        info['r_email'] = attemptObj.email
        info['s'] = "Verification Code - CoolForumSite"
        info['b'] = """
        Here is your verification code:
        {}
        """.format(attemptObj.verification_code)
        
        if not attemptObj.verification_code_email_sent:
            sendGmail(info)
            attemptObj.verification_code_email_sent = True
            attemptObj.save()
        
        
        
        return render(request, 'main/signupProcess/verificationCode.html',x)
        
def resendVerificationCode(request):
    attempt_id = request.session.get('attempt_id')
    attemptObj = SignUpAttempt.objects.get(id=attempt_id)
    
    attemptObj.verification_code_email_sent = False
    attemptObj.verification_code = generateVerificationCode()
    attemptObj.save()
    
    return redirect('main:verification_code')






class ProductList(generic.ListView):
    
    template_name = 'main/productList.html'
    context_object_name = 'productList'
    
    def get_queryset(self):
        return Product.objects.all()
        
class ProductAPIList(APIView):
    
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
# Create your views here.
