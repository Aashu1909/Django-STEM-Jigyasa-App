from django.http.response import HttpResponseRedirect
from django.shortcuts import render,redirect
from django.http import HttpResponse
from JigyasaApp.models import CustomUser, Staff
from django.contrib import messages
def home(request):
    return render(request,'dashboard/admin/home_content.html')

def add_faculty(request):
    return render(request,'dashboard/admin/add_faculty.html')

def add_faculty_save(request):
    if request.method!="POST":
        return HttpResponse("Method not allowed")
    else:
        first_name=request.POST.get('firstName')
        last_name=request.POST.get('lastName')
        email_address=request.POST.get('email')
        username=request.POST.get('username')
        address=request.POST.get('address')
        password=request.POST.get('password')
        cnf_password=request.POST.get('password1')
        if password==cnf_password:
            try:
                user_create=CustomUser.objects.create_user(user_type=2,username=username,first_name=first_name,last_name=last_name,email=email_address,password=cnf_password)
                # user_create.staff .address=address
                user_create .save()
                messages.success(request,"Succesfully Added your details")
                return HttpResponseRedirect('/app/admin_add_faculty_page')
            except:
                messages.error(request,"User details cannot be saved.Please Try Again!!")
                return HttpResponseRedirect('/app/admin_add_faculty_page')
        else:
            messages.error(request,"Passwords Not Matched!!")
            return HttpResponseRedirect('/app/admin_add_faculty_page')

def add_course(request):
    return render(request,'dashboard/admin/add_course.html')

def add_course_save(request):
    pass
