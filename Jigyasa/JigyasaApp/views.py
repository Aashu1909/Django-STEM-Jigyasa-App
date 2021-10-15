from django import http
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import login,logout
from JigyasaApp.custom_backend import EmailBackEnd
from django.contrib import messages
# Create your views here.

# For Faculty sign-up page

def signup_faculty_page(request):
    return render(request, 'JigyasaApp/faculty_signup_page.html')

# admin signup page

def signup_admin_page(request):
    return render(request, 'JigyasaApp/admin_signup_page.html')

# For Student sign-up page

def signup_student_page(request):
    return render(request, 'JigyasaApp/student_signup_page.html')

# Login Pages
# Function for student login page

def student_login_page(request):
    return render(request, 'JigyasaApp/student_login_page.html')

# Function for faculty login page

def faculty_login_page(request):
    return render(request, 'JigyasaApp/faculty_login_page.html')

# admin login page

def admin_login_page(request):
    return render(request, 'JigyasaApp/admin_login_page.html')

# student login

def student_login(request):
    pass

# faculty login

def faculty_login(request):
    print("faculty Login")
    if request == 'POST':
        return HttpResponse('Email:' + request.POST.get('email') + " password:"+request.POST.get('password'))
    else:
        return HttpResponse('Method not allowed')

# admin login


def admin_login(request):
    if request.method != 'POST':
        return HttpResponse('Method not allowed')
    else:
        email=request.POST.get('email')
        password=request.POST.get('password')
        print(email)
        print(password)
        get_user = EmailBackEnd.authenticate(request, username=email, password=password)
        print(get_user)

        if get_user != None:
            login(request,get_user)
            return HttpResponseRedirect('/app/admin_home_page')
        else:
            messages.error(request,"Invalid login Credentials")
            return HttpResponseRedirect('/app/admin_login_page')

# User details Admin
def admin_user_details(request):
    if request.user != None:
        return HttpResponse("User:" + request.user.email + "Usertype:" + request.user.user_type)


def admin_user_logout(request):
    logout(request)
    return HttpResponseRedirect('/app/admin_login_page')

def admin_demo(request):
    return render(request,'dashboard/demo.html')