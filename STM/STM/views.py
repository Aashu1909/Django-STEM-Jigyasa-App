from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from StemApp.models import Contacts


def home_page(request):
    return render(request,'home/index.html')

def contact(request):
    if request.method != "POST":
        messages.error(request, "Inappropriate Method Please Try Again.")
        return HttpResponseRedirect(reverse("homePage"))
    else:
        try:
            # recieved data
            print("contact try")
            r_name=request.POST.get('name')
            r_subject=request.POST.get('subject')
            r_email=request.POST.get('email')
            r_message=request.POST.get('message')
            contact_model = Contacts(name=r_name,subject=r_subject,email=r_email,message=r_message)
            contact_model.save()
            print("contact saved")
            messages.success(request, 'Contact Saved Successfully')
            return HttpResponseRedirect(reverse('homePage'))
        except Exception as e:
            messages.error(request, e)
            return HttpResponseRedirect(reverse('homePage'))