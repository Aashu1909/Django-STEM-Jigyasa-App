from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
def index(request):
    return render(request,'home/index.html')

def contact(request):
    messages.success(request,'Succesfullt send')
    name=request.POST.get('name')
    subject=request.POST.get('subject')
    email=request.POST.get('email')
    message=request.POST.get('message')
    print(name)
    print(subject)
    print(email)
    print(message)
    return HttpResponse("Succesfully Submitted")