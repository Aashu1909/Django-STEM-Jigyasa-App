from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import CustomUser, Staffs, Courses, Students,Subjects
from django.contrib import messages


def home(request):
    return render(request, 'dashboard/admin/home_content.html')


def add_faculty(request):
    return render(request, 'dashboard/admin/add_faculty.html')


def add_faculty_save(request):
    if request.method != "POST":
        return HttpResponse("Method not allowed")
    else:
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        email = request.POST.get('email')
        username = request.POST.get('username')
        address = request.POST.get('address')
        password = request.POST.get('password')
        cnf_password = request.POST.get('password1')
        if password == cnf_password:
            # if you are trying to add details in the models after the user is created the name should be.
            # same as the @receiver create user profile
            try:
                user = CustomUser.objects.create_user(username=username, password=password, email=email,
                                                      last_name=last_name, first_name=first_name, user_type=2)
                user.staffs.address = address
                user.save()
                messages.success(request, "Successfully Added Staff")
                return HttpResponseRedirect("/app/admin_add_faculty_page")
            except:
                messages.error(request, "Failed to Add Staff")
                return HttpResponseRedirect("/app/admin_add_faculty_page")
        else:
            messages.error(request, "Passwords Not Matched!!")
            return HttpResponseRedirect('/app/admin_add_faculty_page')


def add_course(request):
    return render(request, 'dashboard/admin/add_course.html')


def add_course_save(request):
    if request.method != "POST":
        messages.error("Inappropriate Method Please Try Again.")
        return HttpResponseRedirect('/app/admin_add_course_page')
    else:
        try:
            course = request.POST.get('course')
            course_model = Courses(course_name=course)
            course_model.save()
            messages.success(request, 'Course Added Successfully')
            return HttpResponseRedirect('/app/admin_add_course_page')
        except:
            messages.error(request, 'Something Happened Please try again')
            return HttpResponseRedirect('/app/admin_add_course_page')


def add_student(request):
    courses = Courses.objects.all()
    return render(request, 'dashboard/admin/add_student.html', {'courses': courses})


def add_student_save(request):
    if request.method != "POST":
        messages.error(request, 'Method not Allowed')
        return HttpResponse("/app/admin_add_student_page")
    else:
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        email_address = request.POST.get('email')
        username = request.POST.get('username')
        address = request.POST.get('address')
        password = request.POST.get('password')
        course_id = request.POST.get('course')
        session_start = request.POST.get('session_start_date')
        session_end = request.POST.get('session_end_date')
        sex = request.POST.get('sex')
        cnf_password = request.POST.get('password1')
        print(sex)
        if password == cnf_password:
            try:
                user = CustomUser.objects.create_user(user_type=3, username=username, first_name=first_name,
                                                      last_name=last_name, email=email_address, password=cnf_password)
                course_obj = Courses.objects.get(id=course_id)
                user.students.course_id = course_obj
                user.students.gender = sex
                user.students.session_start_year = session_start
                user.students.session_end_year = session_end
                user.students.address = address
                user.students.profile_pic = ""
                user.save()
                messages.success(request, "Successfully Added Student")
                return HttpResponseRedirect('/app/admin_add_student_page')
            except:
                messages.error(request, "Failed To Add Student.Please Try Again!!")
                return HttpResponseRedirect('/app/admin_add_student_page')
        else:
            messages.error(request, "Passwords Not Matched!!")
            return HttpResponseRedirect('/app/admin_add_student_page')


def add_subject(request):
    courses = Courses.objects.all()
    staffs = CustomUser.objects.filter(user_type=2)
    return render(request, 'dashboard/admin/add_subject.html',{'courses':courses,'staffs':staffs})


def add_subject_save(request):
    if request.method != "POST":
        messages.error(request, 'Method not Allowed')
        return HttpResponse("/app/admin_add_subject_page")
    else:
        subject_name = request.POST.get("subject_name")
        course_id = request.POST.get("course")
        course = Courses.objects.get(id=course_id)
        staff_id = request.POST.get("staff")
        staff = CustomUser.objects.get(id=staff_id)

        try:
            subject = Subjects(subject_name=subject_name, course_id=course, staff_id=staff)
            subject.save()
            messages.success(request, "Successfully Added Subject")
            return HttpResponseRedirect("/app/admin_add_subject_page")
        except:
            messages.error(request, "Failed to Add Subject")
            return HttpResponseRedirect("/app/admin_add_subject_page")

def manage_faculty(request):
    staffs=Staffs.objects.all()
    return render(request, 'dashboard/admin/manage_faculty.html',{'staffs':staffs})

def edit_faculty(request):
    pass

def manage_student(request):
    students=Students.objects.all()
    return render(request, 'dashboard/admin/manage_student.html',{'students':students})

def manage_course(request):
    courses=Courses.objects.all()
    return render(request, 'dashboard/admin/manage_course.html',{'courses':courses})

def manage_subject(request):
    subjects=Subjects.objects.all()
    return render(request, 'dashboard/admin/manage_subject.html',{'subjects':subjects})
