from django.contrib import admin
from django.urls import path
from django.conf import settings

from .   import views
urlpatterns = [
     path('demo/',views.demo, name='demo'),
     path('student_login/',views.student_login,name='studentLogin'),
     path('student_login_page/',views.student_login_page, name='studentLoginPage'),
     path('faculty_login_page/',views.faculty_login_page, name='facultyLoginPage'),
     path('faculty_login/',views.faculty_login, name='facultyLogin'),
     path('signup_faculty_page/',views.signup_faculty_page, name='facultySignupPage'),
     path('signup_student_page/',views.signup_student_page, name='studentSignupPage'),
]
