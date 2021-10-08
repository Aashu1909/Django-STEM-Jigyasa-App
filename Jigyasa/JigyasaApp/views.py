from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

# For sign-up
def signup(request):
    return render(request,'sign_up.html')
    
#Function for student login 
def student_login(request):
    return render(request,'JigyasaApp/student_login.html')
# Function for faculty login 
def faculty_login(request):
    return render(request,'JigyasaApp/faculty_login.html')

def test(request):
    return render(request,'JigyasaApp/test.html')
