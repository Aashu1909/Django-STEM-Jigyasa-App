from django import forms
from .models import Courses,SessionYearModel


class DateInput(forms.DateInput):
    input_type = 'date'


class AddStudentForms(forms.Form):
    first_name = forms.CharField(label='First Name', widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Last Name', widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(label='Address', widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-control'}),required=True)
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class':'form-control'}), required=True)
    profile_pic = forms.FileField(label='Profile Pic',widget=forms.FileInput(attrs={'class': 'form-control'}), required=False)
    courses = Courses.objects.all()
    course_list = []
    try:
        for course in courses:
            small_course = (course.id, course.course_name)
            course_list.append(small_course)
    except:
        course_list=[]
    session_list = []
    try:
        sessions=SessionYearModel.objects.all()
        for session in sessions:
            session_start_year = str(session.session_start_year)
            session_start_year = session_start_year[:4]
            session_end_year = str(session.session_end_year)
            session_end_year = session_end_year[:4]
            small_session = (session.id, session_start_year + "-" + session_end_year)
            session_list.append(small_session)
    except:
        session_list=[]
    print(session_list)
    gender_choice = (
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other")
    )
    session_year_id = forms.ChoiceField(label='Select Session', choices=session_list,widget=forms.Select(attrs={'class': 'form-control'}))
    sex = forms.ChoiceField(label='Sex', choices=gender_choice,widget=forms.Select(attrs={'class': 'form-control'}))
    courses = forms.ChoiceField(label='Courses', choices=course_list,widget=forms.Select(attrs={'class': 'form-control'}) )
    password = forms.CharField(label='Enter Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    cnf_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}) )


class EditStudentForms(forms.Form):
    email = forms.EmailField(label='Email',widget=forms.EmailInput(attrs={'class':'form-control'}))
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label='First Name', widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Last Name', widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(label='Address', widget=forms.TextInput(attrs={'class': 'form-control'}))
    profile_pic = forms.FileField(label='Profile Pic', widget=forms.FileInput(attrs={'class': 'form-control'}), required=False)
    courses = Courses.objects.all()
    course_list = []
    for course in courses:
        small_course = (course.id, course.course_name)
        course_list.append(small_course)
    gender_choice = (
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other")
    )
    session_list=[]
    try:
        sessions=SessionYearModel.objects.all()
        for session in sessions:
            session_start_year = str(session.session_start_year)
            session_start_year = session_start_year[:4]
            session_end_year = str(session.session_end_year)
            session_end_year = session_end_year[:4]
            small_session = (session.id, session_start_year + "-" + session_end_year)
            session_list.append(small_session)
    except:
        session_list=[]
    sex = forms.ChoiceField(label='Sex', choices=gender_choice,widget=forms.Select(attrs={'class': 'form-control'}))
    session_year_id = forms.ChoiceField(label='Session Year', choices=session_list, widget=forms.Select(attrs={'class': 'form-control'}))
    courses = forms.ChoiceField(label='Courses', choices=course_list,widget=forms.Select(attrs={'class': 'form-control'}) )
