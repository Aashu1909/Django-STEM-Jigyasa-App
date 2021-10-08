from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from .   import views
urlpatterns = [
     path('student_login/',views.student_login,name='studentLogin'),
     path('',views.test,name='test'),
     path('faculty_login/',views.faculty_login,name='facultyLogin'),
     # path('sign_up/',views.sign_up,name='facultyLogin')
]
