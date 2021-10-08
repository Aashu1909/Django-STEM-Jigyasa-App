from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

# For Faculty sign-up
def Signupfaculty(request):
    return render(request,'JigyasaApp/faculty_signup.html')
    
# For Student sign-up
def Signupstudent(request):
    return render(request,'JigyasaApp/student_signup.html')
    
#Function for student login 
def student_login(request):
    return render(request,'JigyasaApp/student_login.html')

# Function for faculty login 
def faculty_login(request):
    return render(request,'JigyasaApp/faculty_login.html')

def test(request):
    return render(request,'JigyasaApp/test.html')
