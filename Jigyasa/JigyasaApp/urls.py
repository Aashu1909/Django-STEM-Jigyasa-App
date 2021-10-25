from django.contrib import admin
from django.urls import path
from .import Admin_views,Staff_views,Student_views
from .import views
urlpatterns = [
     path('login_page',views.ShowLoginPage,name="ShowLogin"),
     path('doLogin',views.doLogin,name="doLogin"),
     path('logout_user', views.logout_user,name="logout"),
     # path('admin_login/',views.admin_login,name='AdminLogin'),
     # path('admin_login_page/',views.admin_login_page,name='adminLoginPage'),
     # path('admin_user_logout/',views.admin_user_logout,name='AdminLogout'),
     path('admin_user_details/',views.admin_user_details,name='AdminDetails'),
     path('admin_signup_page/',views.signup_admin_page,name='adminSignupPage'),
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
     path('admin_edit_course_save_page/', Admin_views.edit_course_save, name='AdminSaveEditCourse'),
     # admin Student Path
     path('admin_add_student_page/',Admin_views.add_student, name='AdminAddStudent'),
     path('admin_student_save_page/',Admin_views.add_student_save, name='AdminSaveStudent'),
     path('admin_manage_student_page/', Admin_views.manage_student, name='AdminManageStudent'),
     path('admin_edit_student_page/<str:student_id>', Admin_views.edit_student, name='AdminEditStudent'),
     path('admin_edit_student_save_page', Admin_views.edit_student_save, name='AdminSaveEditStudent'),
     # Admin Subject Path
     path('admin_add_subject_page/', Admin_views.add_subject, name='AdminAddSubject'),
     path('admin_add_subject_save_page/', Admin_views.add_subject_save, name='AdminSaveSubject'),
     path('admin_manage_subject_page/', Admin_views.manage_subject, name='AdminManageSubject'),
     path('admin_edit_subject_page/<str:subject_id>/', Admin_views.edit_subject, name='AdminEditSubject'),
     path('admin_edit_subject_save_page/', Admin_views.edit_subject_save, name='AdminSaveEditSubject'),
     # manage session year
     path('admin_manage_session_year_page/', Admin_views.manage_session, name='AdminManageSession'),
     path('admin_session_year_save_page/', Admin_views.manage_session_save, name='AdminManageSessionSave'),

     path('check_user_availabilty/', views.check_user_availability, name='CheckUserAvailabilty'),

         
     # path('faculty_login/',views.faculty_login, name='FacultyLogin'),
     # path('faculty_user_logout/',views.faculty_user_logout,name='FacultyLogout'),
     # path('faculty_login_page/',views.faculty_login_page, name='FacultyLoginPage'),
     path('faculty_signup_page/', views.signup_faculty_page, name='FacultySignupPage'),
     path('faculty_home_page/', Staff_views.faculty_home, name='FacultyHome'),
     path('get_students/', Staff_views.get_students, name="FacultyGetStudents"),
     path('faculty_take_attendance_page/', Staff_views.take_attendance, name='FacultyTakeAttendance'),
     path('faculty_save_attendance_data/', Staff_views.save_attendance, name="FacultySaveAttendance"),
     path('faculty_view_update_attendance_data/', Staff_views.update_attendance, name="FacultyViewUpdateAttendance"),
     path('faculty_get_attendance_dates/', Staff_views.get_attendance, name="FacultyGetAttendance"),
     path('faculty_fetch_student/', Staff_views.fetch_student, name="FacultyFetchStudent"),
     path('faculty_updated_attendance/', Staff_views.updated_attendance, name="FacultyUpdatedAttendance"),

     # path('student_login/',views.student_login,name='StudentLogin'),
     # path('student_user_logout/',views.student_user_logout,name='StudentLogout'),
     # path('student_login_page/',views.student_login_page, name='StudentLoginPage'),
     path('student_signup_page/',views.signup_student_page, name='StudentSignupPage'),
     path('student_home_page/',Student_views.student_home, name='StudentHome'),

]
