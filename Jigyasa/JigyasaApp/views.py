from django import http
from django.http import response
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth import login, logout
from .models import CustomUser
from .custom_backend import EmailBackEnd
from django.contrib import messages
import json

# Create your views here.

# For Faculty sign-up page

def check_user_availability(request):
    if request.method == "POST":
        username = request.POST.get('username')
        print('username:'+str(username))
        all_users=CustomUser.objects.all()
        username_list=[]
        for user in all_users:
            username_list.append(user.username)
        
        if username in username_list:
            status={'status':'no'}
            response=json.dumps(status)
        else:
            status={'status':'yes'}
            response=json.dumps(status)
        return HttpResponse(response)
      
def check_email_availability(request):
    if request.method == "POST":
        username = request.POST.get('username')
        print('username:'+str(username))
        all_users=CustomUser.objects.all()
        username_list=[]
        for user in all_users:
            username_list.append(user.username)
        
        if username in username_list:
            status={'status':'no'}
            response=json.dumps(status)
        else:
            status={'status':'yes'}
            response=json.dumps(status)
        return HttpResponse(response)

def password_reset(request):
    pass

def doLogin(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        user=EmailBackEnd.authenticate(request,username=request.POST.get("email"),password=request.POST.get("password"))
        if user!=None:
            login(request,user)
            if user.user_type=="1":
                return HttpResponseRedirect(reverse('AdminHome'))
            elif user.user_type=="2":
                return HttpResponseRedirect(reverse("FacultyHome"))
            else:
                return HttpResponseRedirect(reverse("StudentHome"))
        else:
            messages.error(request,"Invalid Login Details")
            return HttpResponseRedirect(reverse('ShowLogin'))

def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('ShowLogin'))

def ShowLoginPage(request):
    return render(request, 'JigyasaApp/faculty_login_page.html')


def signup_admin_page(request):
    return render(request, 'JigyasaApp/admin_signup_page.html')

# def admin_login_page(request):
#     return render(request, 'JigyasaApp/admin_login_page.html')

# User details Admin
def admin_user_details(request):
    if request.user != None:
        return HttpResponse("User:" + request.user.email + "Usertype:" + request.user.user_type)

# def admin_user_logout(request):
#     logout(request)
#     return HttpResponseRedirect('/app/admin_login_page')

def admin_demo(request):
    return render(request, 'dashboard/demo.html')


def signup_faculty_page(request):
    return render(request, 'JigyasaApp/faculty_signup_page.html')

# def faculty_login_page(request):
#     return render(request, 'JigyasaApp/faculty_login_page.html')

# def faculty_user_logout(request):
#     logout(request)
#     return HttpResponseRedirect(reverse('FacultyLoginPage'))

def signup_student_page(request):
    return render(request, 'JigyasaApp/student_signup_page.html')

# def student_login_page(request):
#     return render(request, 'JigyasaApp/student_login_page.html')


# def student_user_logout(request):
#     logout(request)
#     return HttpResponseRedirect(reverse('StudentLoginPage'))



# def admin_login(request):
#     if request.method!="POST":
#         return HttpResponse("<h2>Method Not Allowed</h2>")
#     else:
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         print(email)
#         print(password)
#         user=EmailBackEnd.authenticate(request,username=email,password=password)
#         if user!=None:
#             if user.user_type=="1":
#                 login(request,user)
#                 return HttpResponseRedirect(reverse('AdminHome'))
#             else:
#                 messages.error(request,"Invalid Login Details")
#                 return HttpResponseRedirect(reverse('AdminLogin'))
#         else:
#             messages.error(request,"Invalid Login Details")
#             return HttpResponseRedirect(reverse('AdminLogin'))

# def faculty_login(request):
#     if request.method!="POST":
#         messages.error(request,"Not A POST method")
#         return HttpResponseRedirect("FacultyLogin")
#     else:
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         print(email)
#         print(password)
#         user=EmailBackEnd.authenticate(request,username=email,password=password)
#         if user!=None:
#             if user.user_type=="2":
#                 login(request,user)
#                 return HttpResponseRedirect(reverse("FacultyHome"))
#             else:
#                 messages.error(request,"User Not A Faculty.Please Contact your Administrator.")
#                 return HttpResponseRedirect(reverse('FacultyLogin'))
#         else:
#             messages.error(request,"Invalid Login Details")
#             return HttpResponseRedirect("FacultyLogin")

# def student_login(request):
#     if request.method!="POST":
#         print('NotPOst')
#         messages.error(request,"Method NOT POST")
#         return HttpResponseRedirect(reverse('StudentLogin'))
#     else:
#         print('Post')
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         print(email)
#         print(password)
#         user=EmailBackEnd.authenticate(request,username=email,password=password)
#         if user!=None:
#             login(request,user)
#             print('usernotnone')
#             if user.user_type=="3":
#                 return HttpResponseRedirect(reverse('StudentHome'))
#             else:
#                 messages.error(request,"User not a Student.Please contact with the Administrator")
#                 return HttpResponseRedirect(reverse('StudentLogin'))
#         else:
#             messages.error(request,"Invalid Login Details")
#             return HttpResponseRedirect(reverse('StudentLogin'))