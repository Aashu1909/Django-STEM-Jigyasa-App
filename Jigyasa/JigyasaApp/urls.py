from django.contrib import admin
from django.urls import path
from django.conf import settings
from .import Admin_views 
from .import views
urlpatterns = [
    
     path('admin_login/',views.admin_login,name='adminLogin'),
     path('admin_login_page/',views.admin_login_page,name='adminLoginPage'),
     path('admin_signup_page/',views.signup_admin_page,name='adminSignupPage'),
     path('admin_user_details/',views.admin_user_details,name='AdminDetails'),
     path('admin_user_logout/',views.admin_user_logout,name='AdminLogout'),
     path('admin_home_page/',Admin_views.home,name='AdminHome'),
     # Admin Faculty paths
     path('admin_add_faculty_page/',Admin_views.add_faculty, name='AdminAddFaculty'),
     path('admin_add_faculty_save_page/',Admin_views.add_faculty_save, name='AdminSaveFaculty'),
     path('admin_manage_faculty_page/', Admin_views.manage_faculty, name='AdminManageFaculty'),
     path('admin_edit_faculty_page/<str:staff_id>/', Admin_views.edit_faculty, name='AdminEditFaculty'),
     path('admin_edit_faculty_save_page', Admin_views.edit_faculty_save, name='AdminSaveEditFaculty'),
     # Admin course Path
     path('admin_add_course_page/',Admin_views.add_course, name='AdminAddCourse'),
     path('admin_add_course_save_page/',Admin_views.add_course_save, name='AdminSaveCourse'),
     path('admin_manage_course_page/',Admin_views.manage_course, name='AdminManageCourse'),
     path('admin_edit_course_page/<str:course_id>/',Admin_views.edit_course, name='AdminEditCourse'),
     path('admin_edit_course_save_page/',Admin_views.edit_course_save, name='AdminSaveEditCourse'),
     # admin Student Path
     path('admin_add_student_page/',Admin_views.add_student, name='AdminAddStudent'),
     path('admin_student_save_page/',Admin_views.add_student_save, name='AdminSaveStudent'),
     path('admin_manage_student_page/', Admin_views.manage_student, name='AdminManageStudent'),
     path('admin_edit_student_page/<str:student_id>/', Admin_views.edit_student, name='AdminEditStudent'),
     path('admin_edit_student_save_page', Admin_views.edit_student_save, name='AdminSaveEditStudent'),
     # Admin Subject Path
     path('admin_add_subject_page/',Admin_views.add_subject, name='AdminAddSubject'),
     path('admin_add_subject_save_page/',Admin_views.add_subject_save, name='AdminSaveSubject'),
     path('admin_manage_subject_page/',Admin_views.manage_subject, name='AdminManageSubject'),
     path('admin_edit_subject_page/<str:subject_id>/',Admin_views.edit_subject, name='AdminEditSubject'),
     path('admin_edit_subject_save_page/',Admin_views.edit_subject_save, name='AdminSaveEditSubject'),
     
     path('check_user_availabilty/',views.check_user_availability, name='CheckUserAvailabilty'),    

     path('student_login/',views.student_login,name='studentLogin'),
     path('student_login_page/',views.student_login_page, name='studentLoginPage'),
     path('student_signup_page/',views.signup_student_page, name='studentSignupPage'),
     
     path('faculty_login_page/',views.faculty_login_page, name='facultyLoginPage'),
     path('faculty_login/',views.faculty_login, name='facultyLogin'),
     path('faculty_signup_page/',views.signup_faculty_page, name='facultySignupPage'),
        
]
