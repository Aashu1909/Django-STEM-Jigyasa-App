from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

# For Faculty sign-up page
def signup_faculty_page(request):
    return render(request,'JigyasaApp/faculty_signup.html')
    
# For Student sign-up page
def signup_student_page(request):
    return render(request,'JigyasaApp/student_signup.html')
    
#Function for student login page 
def student_login_page(request):
    return render(request,'JigyasaApp/student_login.html')
# student login
def student_login(request):
    print("Student Login")
    print(request)
    if request.method=="POST":
        email=request.POST.get('email','')
        password=request.POST.get('password','')
        print(email)
        print(password)
    else:
        print('method not allowed')    


# Function for faculty login page
def faculty_login_page(request):
    return render(request,'JigyasaApp/faculty_login.html')

def faculty_login(request):
    print("faculty Login")
    if request=='POST':
        return HttpResponse('Email:'+ request.POST.get('email') + " password:"+request.POST.get('password') )
    else:
        return HttpResponse('Method not allowed')

def demo(request):
    return render(request,'dashboard/demo.html')
