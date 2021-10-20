from django import forms
from .models import Courses


class AddStudentForms(forms.Form):
    email=forms.EmailField(label='Email',max_length=50)
    first_Name=forms.CharField(label='FirstName',max_length=50)
    lastName=forms.CharField(label='LastName',max_length=50)
    address=forms.CharField(label='Address',max_length=50)
    gender_choice=[
        'Male','Female','Others'
    ]
    sex=forms.ChoiceField(label='Sex',choices=gender_choice)

    course_list=[]
    courses=Courses.objects.all()
    for course in courses:
        small_course=(course.id,course.course_name)
        course_list.append(small_course)

    course=forms.ChoiceField(label='Course',choices=course_list)
    session_start_date=forms.DateField(label='Session Start')
    session_end_date=forms.DateField(label='Session End')
    username=forms.CharField(label='Username',max_length=50)
    profile_pic=forms.FileField(label='Profile Pic',max_length=50)
    password=forms.CharField(label='Enter Password',max_length=50)
    password1=forms.CharField(label='Confirm Password',max_length=50)
     