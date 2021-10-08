from django.contrib import admin
from django.urls import path
from django.conf import settings

from .   import views
urlpatterns = [
     path('student_login/',views.student_login, name='studentLogin'),
     path('faculty_login/',views.faculty_login, name='facultyLogin'),
     path('signup_faculty/',views.Signupfaculty, name='facultySignup'),
     path('signup_student/',views.Signupstudent, name='studentSignup'),
]
