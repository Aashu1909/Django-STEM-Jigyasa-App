import datetime
from django.contrib import messages
from django.http.response import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from django.urls.base import reverse
from .models import Attendance, AttendanceReport, Courses, CustomUser, FeedBackStudent, Students, Subjects,LeaveReportStudent

def student_home(request):
    if str(request.user.user_type) =='3':
        custom_obj=CustomUser.objects.get(id=request.user.id)
        student_obj=Students.objects.get(admin=custom_obj)
        attendance_total=AttendanceReport.objects.filter(student_id=student_obj).count()
        attendance_present=AttendanceReport.objects.filter(student_id=student_obj,status=True).count()
        attendance_absent=AttendanceReport.objects.filter(student_id=student_obj,status=False).count()
        course=Courses.objects.get(id=student_obj.course_id.id)
        subject=Subjects.objects.filter(course_id=course).count()
        subject_name=[]
        data_absent=[]
        data_present=[]
        subjects_data=Subjects.objects.filter(course_id=student_obj.course_id)
        for subject in subjects_data:
            attendance=Attendance.objects.filter(subject_id=subject.id)
            attendance_present_count=AttendanceReport.objects.filter(attendance_id__in=attendance,status=True).count()
            attendance_absent_count=AttendanceReport.objects.filter(attendance_id__in=attendance,status=False).count()
            subject_name.append(subject.subject_name)
            data_present.append(attendance_present_count)
            data_absent.append(attendance_absent_count)
        params={
            'total_attendance':attendance_total,
            'present':attendance_present,
            'absent':attendance_absent,
            'subjects':len(subject_name),
            'subject_name':subject_name,
            'attendance_present':data_present,
            'attendance_absent':data_absent
        }
        return render(request, 'dashboard/student_templates/home_content.html',params)
    else: 
        return HttpResponse(reverse('ShowLogin'))

def edit_profile(request):
    user=CustomUser.objects.get(id=request.user.id)
    param={
        'user':user
    }
    return render(request,'dashboard/admin/edit_profile.html',param)

def edit_profile_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("StudentEditProfile"))
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        password=request.POST.get("password")
        try:
            customuser=CustomUser.objects.get(id=request.user.id)
            customuser.first_name=first_name
            customuser.last_name=last_name
            
            customuser.save()
            messages.success(request, "Successfully Updated Profile")
            return HttpResponseRedirect(reverse("StudentEditProfile"))
        except:
            messages.error(request, "Failed to Update Profile")
            return HttpResponseRedirect(reverse("StudentEditProfile"))

def view_attendance(request):
    user_obj=CustomUser.objects.get(id=request.user.id)
    student_obj=Students.objects.get(admin=user_obj)
    course_obj=Courses.objects.get(id=student_obj.course_id.id)
    subject_obj=Subjects.objects.filter(course_id=course_obj)
    param={
        'course':course_obj,
        'subjects':subject_obj
    }
    return render(request, 'dashboard/student_templates/student_view_attendance.html',param)
    
def view_attendence_get(request):
    if request.method!="POST":
        return HttpResponse("Method not allowed")
    else:
        subject_id = request.POST.get('subject_id')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        # Parsing Date into yyyy-mm-dd format
        start_date_parse=datetime.datetime.strptime(start_date,'%Y-%m-%d').date()
        end_date_parse=datetime.datetime.strptime(end_date,'%Y-%m-%d').date()
        subject_obj=Subjects.objects.get(id=subject_id)
        user_obj=CustomUser.objects.get(id=request.user.id)
        student_obj=Students.objects.get(admin=user_obj)
        # here __range is used to pass the range value.
        attendance_obj=Attendance.objects.filter(attendance_date__range=(start_date_parse,end_date_parse),
        subject_id=subject_obj)
        # here __in query is same as Sql Query "where FIELD in ()"
        attendance_reports_obj=AttendanceReport.objects.filter(attendance_id__in=attendance_obj,student_id=student_obj)
        param={
            'attendance_reports':attendance_reports_obj
        }
        return render(request,'dashboard/student_templates/student_view_attendance_data.html',param)


def apply_leave(request):
    admin_obj=CustomUser.objects.get(id=request.user.id)
    student_obj=Students.objects.get(admin=admin_obj)
    prev_leave_data=LeaveReportStudent.objects.filter(student_id=student_obj)
    param={
        'prev_leave_data':prev_leave_data
    }
    return render(request,'dashboard/student_templates/student_apply_leave.html',param)

def apply_leave_save(request):
    if request.method != "POST":
        return HttpResponse("Method not allowed")
    else:
        leave_date = request.POST.get('leave_date')
        leave_reason = request.POST.get('leave_reason')
        try:
            admin_obj=CustomUser.objects.get(id=request.user.id)
            student_obj = Students.objects.get(admin=admin_obj)
            leave_report_obj=LeaveReportStudent(student_id=student_obj,leave_date=leave_date,leave_message=leave_reason)
            leave_report_obj.save()
            messages.success(request, "Succesfully Applied Leave Application")
            return HttpResponseRedirect(reverse('StudentApplyLeave'))
        except Exception as e:
            messages.error(request, e)
            return HttpResponseRedirect(reverse('StudentApplyLeave'))

def feedback_menu(request):
    admin_obj=CustomUser.objects.get(id=request.user.id)
    student_obj=Students.objects.get(admin=admin_obj)
    prev_feedback_data=FeedBackStudent.objects.filter(student_id=student_obj)
    param={
        'feedbacks':prev_feedback_data
    }
    return render(request,'dashboard/student_templates/student_feedback_page.html',param)

def feedback_save(request):
    if request.method != "POST":
        return HttpResponse("Method not allowed")
    else:
        feedback_message = request.POST.get('feedback_message')
        try:
            admin_obj=CustomUser.objects.get(id=request.user.id)
            student_obj = Students.objects.get(admin=admin_obj)
            feedback_obj=FeedBackStudent(student_id=student_obj,feedback=feedback_message)
            feedback_obj.save()
            messages.success(request, "Feedsback Recieved")
            return HttpResponseRedirect(reverse('StudentFeedbackMenu'))
        except Exception as e:
            messages.error(request, e)
            return HttpResponseRedirect(reverse('StudentFeedbackMenu'))