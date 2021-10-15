from django.contrib import admin
from django.urls import path
from django.conf import settings
from .import Admin_views 
from .import views
urlpatterns = [
     path('admin_demo/',views.admin_demo,name='admindemo'),
     path('admin_login/',views.admin_login,name='adminLogin'),
     path('admin_login_page/',views.admin_login_page,name='adminLoginPage'),
     path('admin_signup_page/',views.signup_admin_page,name='adminSignupPage'),
     path('admin_user_details/',views.admin_user_details,name='adminDetails'),
     path('admin_user_logout/',views.admin_user_logout,name='adminLogout'),
     path('admin_home_page/',Admin_views.home,name='adminHome'),
     path('admin_add_faculty_page/',Admin_views.add_faculty, name='AdminAddFaculty'),
 
     path('student_login/',views.student_login,name='studentLogin'),
     path('student_login_page/',views.student_login_page, name='studentLoginPage'),
     path('student_signup_page/',views.signup_student_page, name='studentSignupPage'),
     
     path('faculty_login_page/',views.faculty_login_page, name='facultyLoginPage'),
     path('faculty_login/',views.faculty_login, name='facultyLogin'),
     path('faculty_signup_page/',views.signup_faculty_page, name='facultySignupPage'),
        
]
