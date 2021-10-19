from django.db import reset_queries
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import CustomUser, Staffs, Courses, Students, Subjects
from django.contrib import messages
from django.core.files.storage import FileSystemStorage

def home(request):
    return render(request, 'dashboard/admin/home_content.html')

# Staffs
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

def manage_faculty(request):
    staffs = Staffs.objects.all()
    return render(request, 'dashboard/admin/manage_faculty.html', {'staffs': staffs})

def edit_faculty(request, staff_id):

    staff_user = Staffs.objects.get(admin=staff_id)
    return render(request, 'dashboard/admin/edit_faculty.html', {'staff': staff_user})

def edit_faculty_save(request):
    if request.method != "POST":
        return HttpResponse("Method not allowed")
    else:
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        email = request.POST.get('email')
        address = request.POST.get('address')
        staff_id = request.POST.get('staff_id')
        try:
            curr_user_obj = CustomUser.objects.get(id=staff_id)
            curr_user_obj.first_name = first_name
            curr_user_obj.last_name = last_name
            curr_user_obj.email = email
            curr_user_obj.save()

            curr_staff_obj = Staffs.objects.get(admin=staff_id)
            curr_staff_obj.address = address
            curr_staff_obj.save()

            messages.success(request, "Changes Successfully Added.")
            return HttpResponseRedirect("/app/admin_edit_faculty_page/"+staff_id+"/")
        except:
            messages.error(request, "Failed to Save Changes")
            return HttpResponseRedirect("/app/admin_edit_faculty_page/"+staff_id+"/")


# Students
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
        profile_pic = request.FILES['profile_pic']
        fs = FileSystemStorage()
        filename = fs.save(profile_pic.name, profile_pic)
        profile_pic_url = fs.url(filename)
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
                user.students.profile_pic = profile_pic_url
                user.save()
                messages.success(request, "Successfully Added Student")
                return HttpResponseRedirect('/app/admin_add_student_page')
            except:
                messages.error(
                    request, "Failed To Add Student.Please Try Again!!")
                return HttpResponseRedirect('/app/admin_add_student_page')
        else:
            messages.error(request, "Passwords Not Matched!!")
            return HttpResponseRedirect('/app/admin_add_student_page')

def manage_student(request):
    students = Students.objects.all()
    return render(request, 'dashboard/admin/manage_student.html', {'students': students})

def edit_student(request, student_id):
    curr_student_object = Students.objects.get(admin=student_id)
    courses = Courses.objects.all()
    return render(request, 'dashboard/admin/edit_student.html', {'student': curr_student_object, 'courses': courses})

def edit_student_save(request):
    if request.method != "POST":
        return HttpResponse("Method not allowed")
    else:
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        email = request.POST.get('email')
        address = request.POST.get('address')
        username = request.POST.get('username')
        prev_session_start = request.POST.get('curr_session_start_date')
        prev_session_end = request.POST.get('curr_session_end_date')
        curr_session_start = request.POST.get('change_session_start_date')
        curr_session_end = request.POST.get('change_session_end_date')
        change_course_id = request.POST.get('change_course')
        student_id = request.POST.get('student_id')
        print(str(request.FILES.get('profile_picture')))
        if request.FILES.get('profile_picture',False):
                profile_pic=request.FILES.get('profile_picture')
                fs=FileSystemStorage()
                filename=fs.save(profile_pic.name,profile_pic)
                profile_pic_url=fs.url(filename)
        else:
            profile_pic_url = None

        try:
            curr_user_obj = CustomUser.objects.get(id=student_id)
            curr_user_obj.first_name = first_name
            curr_user_obj.last_name = last_name
            curr_user_obj.email = email
            if username != curr_user_obj.username:
                curr_user_obj.username = username
            curr_user_obj.save()

            curr_student_obj = Students.objects.get(admin=student_id)
            curr_student_obj.address = address

            if profile_pic_url != None:
                curr_student_obj.profile_pic = profile_pic_url

            if curr_session_start != prev_session_start:
                curr_student_obj.session_start_year = curr_session_start
            if curr_session_end != prev_session_end:
                curr_student_obj.session_end_year = curr_session_end

            curr_course_obj = Courses.objects.get(id=change_course_id)
            curr_student_obj.course_id = curr_course_obj
            curr_student_obj.save()

            messages.success(request, "Changes Successfully Added.")
            return HttpResponseRedirect("/app/admin_edit_student_page/"+student_id+"/")
        except:
            messages.error(request, "Failed to Save Changes")
            return HttpResponseRedirect("/app/admin_edit_student_page/"+student_id+"/")


# Courses 
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

def manage_course(request):
    courses = Courses.objects.all()
    return render(request, 'dashboard/admin/manage_course.html', {'courses': courses})

def edit_course(request, course_id):
    course=Courses.objects.get(id=course_id)
    return render(request,'dashboard/admin/edit_course.html',{'course':course})

def edit_course_save(request):
    if request.method != "POST":
        return HttpResponse("Method not allowed")
    else:
        course_id = request.POST.get('course_id')
        print(course_id)
        course_name = request.POST.get('course_name')
        print(course_name)
        try:
            curr_course_obj = Courses.objects.get(id=course_id)
            curr_course_obj.course_name=course_name
            curr_course_obj.save()
            messages.success(request, "Changes Successfully Added.")
            return HttpResponseRedirect("/app/admin_edit_course_page/"+course_id+"/")
        except:
            messages.error(request, "Failed to Save Changes")
            return HttpResponseRedirect("/app/admin_edit_courset_page/"+course_id+"/")


# Subjects 
def add_subject(request):
    courses = Courses.objects.all()
    staffs = CustomUser.objects.filter(user_type=2)
    return render(request, 'dashboard/admin/add_subject.html', {'courses': courses, 'staffs': staffs})

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
            subject = Subjects(subject_name=subject_name,
                               course_id=course, staff_id=staff)
            subject.save()
            messages.success(request, "Successfully Added Subject")
            return HttpResponseRedirect("/app/admin_add_subject_page")
        except:
            messages.error(request, "Failed to Add Subject")
            return HttpResponseRedirect("/app/admin_add_subject_page")

def manage_subject(request):
    subjects = Subjects.objects.all()
    return render(request, 'dashboard/admin/manage_subject.html', {'subjects': subjects})

def edit_subject(request, subject_id):
    subject=Subjects.objects.get(id=subject_id)
    course=Courses.objects.all()
    staff=CustomUser.objects.filter(user_type=2)
    dict={'subject':subject,'courses':course,'staffs':staff}
    return render(request,'dashboard/admin/edit_subject.html',dict)

def edit_subject_save(request):
    if request.method != "POST":
        return HttpResponse("Method not allowed")
    else:
        course_id=request.POST.get('course_id')
        curr_staff_id=request.POST.get('curr_staff')
        change_staff_id=request.POST.get('change_staff')
        subject_name=request.POST.get('subject_name')
        subject_id=request.POST.get('subject_id')
        print(subject_id,subject_name,change_staff_id,curr_staff_id,course_id)
        try:
            subject=Subjects.objects.get(id=subject_id)
            subject.subject_name=subject_name
            course=Courses.objects.get(id=course_id)
            subject.course_id=course
            if str(change_staff_id)!=str(curr_staff_id):
                staff_id=CustomUser.objects.get(id=change_staff_id)
            else:
                staff_id=CustomUser.objects.get(id=curr_staff_id)
            
            subject.staff_id=staff_id
            subject.save()
            messages.success(request, "Changes Successfully Added.")
            return HttpResponseRedirect("/app/admin_edit_subject_page/"+subject_id+"/")
        except:
            messages.error(request, "Failed to Save Changes")
            return HttpResponseRedirect("/app/admin_edit_subject_page/"+subject_id+"/")
