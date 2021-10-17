from django.contrib import admin
from django.urls import path
from django.conf import settings
from .import Admin_views 
from .import views
urlpatterns = [
    
     path('admin_login/',views.admin_login,name='adminLogin'),
     path('admin_login_page/',views.admin_login_page,name='adminLoginPage'),
     path('admin_signup_page/',views.signup_admin_page,name='adminSignupPage'),
     path('admin_user_details/',views.admin_user_details,name='adminDetails'),
     path('admin_user_logout/',views.admin_user_logout,name='adminLogout'),
     path('admin_home_page/',Admin_views.home,name='adminHome'),
     
     path('admin_add_faculty_page/',Admin_views.add_faculty, name='AdminAddFaculty'),
     path('admin_add_faculty_save_page/',Admin_views.add_faculty_save, name='AdminSaveFaculty'),
     path('admin_manage_faculty_page/', Admin_views.manage_faculty, name='AdminManageFaculty'),
     path('admin_edit_faculty_page/', Admin_views.edit_faculty, name='AdminEditFaculty'),
     
     path('admin_add_course_page/',Admin_views.add_course, name='AdminAddCourse'),
     path('admin_add_course_save_page/',Admin_views.add_course_save, name='AdminSaveCourse'),
     path('admin_manage_course_page/',Admin_views.manage_course, name='AdminManageCourse'),
     
     path('admin_add_student_page/',Admin_views.add_student, name='AdminAddStudent'),
     path('admin_student_save_page/',Admin_views.add_student_save, name='AdminSaveStudent'),
     path('admin_manage_student_page/', Admin_views.manage_student, name='AdminManageStudent'),

     path('admin_add_subject_page/',Admin_views.add_subject, name='AdminAddSubject'),
     path('admin_add_subject_save_page/',Admin_views.add_subject_save, name='AdminSaveSubject'),
     path('admin_manage_subject_page/',Admin_views.manage_subject, name='AdminManageSubject'),
     
     

     path('student_login/',views.student_login,name='studentLogin'),
     path('student_login_page/',views.student_login_page, name='studentLoginPage'),
     path('student_signup_page/',views.signup_student_page, name='studentSignupPage'),
     
     path('faculty_login_page/',views.faculty_login_page, name='facultyLoginPage'),
     path('faculty_login/',views.faculty_login, name='facultyLogin'),
     path('faculty_signup_page/',views.signup_faculty_page, name='facultySignupPage'),
        
]
