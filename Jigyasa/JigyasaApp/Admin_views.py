from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse
from .models import CustomUser, Staffs, Courses, Students, Subjects, SessionYearModel
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from .forms import AddStudentForms, EditStudentForms
from django.urls import reverse


def home(request):
    return render(request, 'dashboard/admin/home_content.html')


# Staffs
def add_faculty(request):
    return render(request, 'dashboard/admin/add_templates/add_faculty.html')


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
                return HttpResponseRedirect("/app/admin_add_faculty_page")  # urls path inside Http responmse not
            except Exception as e:
                messages.error(request, e)
                return HttpResponseRedirect(reverse('AdminAddFaculty'))
        else:
            messages.error(request, "Passwords Not Matched!!")
            return HttpResponseRedirect(reverse('AdminAddFaculty'))


def manage_faculty(request):
    staffs = Staffs.objects.all()
    return render(request, 'dashboard/admin/manage_templates/manage_faculty.html', {'staffs': staffs})


def edit_faculty(request, staff_id):
    staff_user = Staffs.objects.get(admin=staff_id)
    return render(request, 'dashboard/admin/edit_templates/edit_faculty.html', {'staff': staff_user, 'id': staff_id})


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
            return HttpResponseRedirect(reverse('AdminEditFaculty', kwargs={'staff_id': staff_id}))
        except Exception as e:
            messages.error(request, e)
            return HttpResponseRedirect(reverse('AdminEditFaculty', kwargs={'staff_id': staff_id}))


# Students
def add_student(request):
    courses = Courses.objects.all()
    form = AddStudentForms()
    param = {'courses': courses, 'form': form}
    return render(request, 'dashboard/admin/add_templates/add_student.html', param)


def add_student_save(request):
    if request.method != "POST":
        messages.error(request, 'Method not Allowed')
        return HttpResponse("/app/admin_add_student_page")
    else:
        form = AddStudentForms(request.POST, request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email_address = form.cleaned_data['email']
            username = form.cleaned_data['username']
            address = form.cleaned_data['address']
            password = form.cleaned_data['password']
            course_id = form.cleaned_data['courses']
            session_id = form.cleaned_data['session_year_id']
            sex = form.cleaned_data['sex']
            cnf_password = form.cleaned_data['cnf_password']
            print(sex)
            print(password)
            print(cnf_password)
            profile_pic = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name, profile_pic)
            profile_pic_url = fs.url(filename)
            if password == cnf_password:
                try:
                    user = CustomUser.objects.create_user(user_type=3, username=username, first_name=first_name,
                                                          last_name=last_name, email=email_address,
                                                          password=cnf_password)
                    course_obj = Courses.objects.get(id=course_id)
                    user.students.course_id = course_obj
                    user.students.gender = sex
                    session=SessionYearModel.objects.get(id=session_id)
                    user.students.session_year = session
                    user.students.address = address
                    user.students.profile_pic = profile_pic_url
                    user.save()
                    messages.success(request, "Successfully Added Student")
                    return HttpResponseRedirect('/app/admin_add_student_page')
                except Exception as e:
                    messages.error(request, e)
                    return HttpResponseRedirect('/app/admin_add_student_page')
            else:
                messages.error(request, "Passwords Not Matched!!")
                return HttpResponseRedirect('/app/admin_add_student_page')
        else:
            print('Not valid')
            form = AddStudentForms(request.POST)
            return render(request, 'dashboard/admin/add_templates/add_student.html', {'form': form})


def manage_student(request):
    students = Students.objects.all()
    return render(request, 'dashboard/admin/manage_templates/manage_student.html', {'students': students})


def edit_student(request, student_id):
    request.session['student_id'] = student_id
    curr_student_object = Students.objects.get(admin=student_id)
    form = EditStudentForms()
    form.fields['first_name'].initial = curr_student_object.admin.first_name
    form.fields['last_name'].initial = curr_student_object.admin.last_name
    form.fields['address'].initial = curr_student_object.address
    form.fields['username'].initial = curr_student_object.admin.username
    form.fields['email'].initial = curr_student_object.admin.email
    form.fields['courses'].initial = curr_student_object.course_id.id
    form.fields['sex'].initial = curr_student_object.gender
    form.fields['session_year_id'].initial=curr_student_object.session_year_id.id
    params = {'form': form, 'id': student_id, 'username': curr_student_object.admin.username}
    return render(request, 'dashboard/admin/edit_templates/edit_student.html', params)


def edit_student_save(request):
    if request.method != "POST":
        return HttpResponse("Method not allowed")
    else:
        student_id = request.session.get('student_id')
        if student_id is None:
            print('Studentid None')
            return HttpResponseRedirect("/app/admin_manage_student_page/")

        form = EditStudentForms(request.POST, request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            address = form.cleaned_data["address"]
            session_year_id = form.cleaned_data["session_year_id"]
            course_id = form.cleaned_data["courses"]
            sex = form.cleaned_data["sex"]
            print(str(request.FILES.get('profile_picture')))
            if request.FILES.get('profile_picture', False):
                profile_pic = request.FILES.get('profile_picture')
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name, profile_pic)
                profile_pic_url = fs.url(filename)
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
                session=SessionYearModel.objects.get(id=session_year_id)
                curr_student_obj.session_year_id = session
                if profile_pic_url is not None:
                    curr_student_obj.profile_pic = profile_pic_url

                curr_course_obj = Courses.objects.get(id=course_id)
                curr_student_obj.course_id = curr_course_obj
                curr_student_obj.save()
                del request.session['student_id']
                messages.success(request, "Changes Successfully Added.")
                return HttpResponseRedirect(reverse('AdminEditStudent',kwargs={'student_id': student_id}))
            except Exception as e:
                messages.error(request, e)
                return HttpResponseRedirect(reverse('AdminEditStudent',  kwargs={'student_id': student_id}))
        else:
            form = EditStudentForms(request.POST, request.FILES)
            student = Students.objects.get(admin=student_id)
            params = {'form': form, 'id': student_id, 'username': student.admin.username}
            return render(request, 'dashboard/admin/edit_templates/edit_student.html', params)


# Courses
def add_course(request):
    return render(request, 'dashboard/admin/add_templates/add_course.html')


def add_course_save(request):
    if request.method != "POST":
        messages.error(request, "Inappropriate Method Please Try Again.")
        return HttpResponseRedirect(reverse("AdminAddCourse"))
    else:
        try:
            course = request.POST.get('course')
            course_model = Courses(course_name=course)
            course_model.save()
            messages.success(request, 'Course Added Successfully')
            return HttpResponseRedirect(reverse('AdminAddCourse)'))
        except Exception as e:
            messages.error(request, e)
            return HttpResponseRedirect(reverse('AdminAddCourse)'))


def manage_course(request):
    courses = Courses.objects.all()
    return render(request, 'dashboard/admin/manage_templates/manage_course.html', {'courses': courses})


def edit_course(request, course_id):
    course = Courses.objects.get(id=course_id)
    return render(request, 'dashboard/admin/edit_templates/edit_course.html', {'course': course, 'id': course_id})


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
            curr_course_obj.course_name = course_name
            curr_course_obj.save()
            messages.success(request, "Changes Successfully Added.")
            return HttpResponseRedirect(reverse('AdminEditCourse',  kwargs={'course_id': course_id}))
        except Exception as e:
            messages.error(request, e)
            return HttpResponseRedirect(reverse('AdminEditCourse', kwargs={'course_id': course_id}))


# Subjects 
def add_subject(request):
    courses = Courses.objects.all()
    staffs = CustomUser.objects.filter(user_type=2)
    return render(request, 'dashboard/admin/add_templates/add_subject.html', {'courses': courses, 'staffs': staffs})


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
            return HttpResponseRedirect(reverse('AdminAddSubject'))
        except Exception as e:
            messages.error(request, e)
            return HttpResponseRedirect(reverse('AdminAddSubject'))


def manage_subject(request):
    subjects = Subjects.objects.all()
    return render(request, 'dashboard/admin/manage_templates/manage_subject.html', {'subjects': subjects})


def edit_subject(request, subject_id):
    subject = Subjects.objects.get(id=subject_id)
    course = Courses.objects.all()
    staff = CustomUser.objects.filter(user_type=2)
    params = {'subject': subject, 'courses': course, 'staffs': staff, 'id': subject_id}
    return render(request, 'dashboard/admin/edit_templates/edit_subject.html', params)


def edit_subject_save(request):
    if request.method != "POST":
        return HttpResponse("Method not allowed")
    else:
        course_id = request.POST.get('course_id')
        curr_staff_id = request.POST.get('curr_staff')
        change_staff_id = request.POST.get('change_staff')
        subject_name = request.POST.get('subject_name')
        subject_id = request.POST.get('subject_id')
        print(subject_id, subject_name, change_staff_id, curr_staff_id, course_id)
        try:
            subject = Subjects.objects.get(id=subject_id)
            subject.subject_name = subject_name
            course = Courses.objects.get(id=course_id)
            subject.course_id = course
            if str(change_staff_id) != str(curr_staff_id):
                staff_id = CustomUser.objects.get(id=change_staff_id)
            else:
                staff_id = CustomUser.objects.get(id=curr_staff_id)

            subject.staff_id = staff_id
            subject.save()
            messages.success(request, "Changes Successfully Added.")
            return HttpResponseRedirect('/app/admin_edit_subject_page/'+subject_id+"/")
        except Exception as e:
            messages.error(request, e)
            return HttpResponseRedirect('/app/admin_edit_subject_page/'+subject_id+"/")


def manage_session(request):
    return render(request, 'dashboard/admin/manage_templates/manage_session_year.html')


def manage_session_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("ManageSession"))
    else:
        print('manage session save')
        session_start_year = request.POST.get("session_start")
        session_end_year = request.POST.get("session_end")
        print(session_start_year)
        print(session_end_year)
        try:
            session_year = SessionYearModel(session_start_year=session_start_year, session_end_year=session_end_year)
            session_year.save()
            messages.success(request, "Successfully Added Session")
            return HttpResponseRedirect(reverse("AdminManageSession"))
        except Exception as e:
            messages.error(request, e)
            return HttpResponseRedirect(reverse("AdminManageSession"))
