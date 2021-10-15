from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request,'dashboard/admin/home_content.html')

def add_faculty(request):
    return render(request,'dashboard/admin/add_staff.html')