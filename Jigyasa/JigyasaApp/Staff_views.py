from django.core.files.storage import FileSystemStorage
from django.http.response import HttpResponse,JsonResponse,HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from .models import * 
from django.views.decorators.csrf import csrf_exempt
import json
from .zoom_meeting import createMeeting

def faculty_home(request):
    # First This is to find how many student are studying under one faculty member.
    admin_staff_obj=CustomUser.objects.get(id=request.user.id)
    staff_obj=Staffs.objects.get(admin=admin_staff_obj)
    subject_obj=Subjects.objects.filter(staff_id=staff_obj.admin.id)
    # Total Subject count.
    subject_obj_count=Subjects.objects.filter(staff_id=staff_obj.admin.id).count()
    course_id_list=[]
    subject_id_list=[]
    subject_name_list=[]
    attendance_list_count=[]
    
    for subject in subject_obj:
        # Now from the subject object getting the Course and hence getting the student.
        course_obj=Courses.objects.get(id=subject.course_id.id)
        # Here we are appending the Course id
        course_id_list.append(course_obj.id)
        if subject.id not in subject_id_list:
            # getting there ids
            subject_id_list.append(subject.id)
            # Getting the  name of subjects
            subject_name_list.append(subject.subject_name)
        # getting te count of student present in each subject Classes.
        attendance_obj_count=Attendance.objects.filter(subject_id=subject.id).count()
        attendance_list_count.append(attendance_obj_count)
    # Now Making the final course list

    final_course=[]
    for course_id in course_id_list:
        if course_id not in final_course:
            final_course.append(course_id)
    # Now finally filtering the Student from Studnet table
    
    student_attendance=Students.objects.filter(course_id__in=final_course)
    student_list=[]
    student_present_list=[]
    student_absent_list=[]
    for student in student_attendance:
        attendance_present=AttendanceReport.objects.filter(status=True,student_id=student.id).count()
        attendance_absent=AttendanceReport.objects.filter(status=False,student_id=student.id).count()
        student_name=str(student.admin.first_name)+" "+str(student.admin.last_name)
        student_list.append(student_name)
        student_present_list.append(attendance_present)
        student_absent_list.append(attendance_absent)
    
    student_count=Students.objects.filter(course_id__in=final_course).count()
    attendance_count=Attendance.objects.filter(subject_id__in=subject_id_list).count()
    leave_total=LeaveReportStaff.objects.filter(staff_id=staff_obj).count()
    leave_approved=LeaveReportStaff.objects.filter(staff_id=staff_obj,leave_status=1).count()
    leave_disapproved=LeaveReportStaff.objects.filter(staff_id=staff_obj,leave_status=2).count()
    params={
        'student_list':student_list,
        'student_present_list':student_present_list,
        'student_absent_list':student_absent_list,
        'total_student_count':student_count,
        'total_subject_count':subject_obj_count,
        'total_attendance_count':attendance_count,
        'total_leave_applied':leave_total,
        'total_leave_approved':leave_approved,
        'total_leave_diapproved':leave_disapproved,
        'subject_name_list':subject_name_list, 
        'subject_wise_attendance':attendance_list_count
    }
    return render(request, 'dashboard/staff_templates/home_content.html',params)

def todo_list(request):
    return render(request,'dashboard/staff_templates/staff_todo_list.html')

def edit_profile(request):
    user=CustomUser.objects.get(id=request.user.id)
    param={
        'user':user
    }
    return render(request,'dashboard/staff_templates/edit_profile.html',param)


def edit_profile_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("StaffEditProfile"))
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        
        try:
            customuser=CustomUser.objects.get(id=request.user.id)
            customuser.first_name=first_name
            customuser.last_name=last_name
            
            customuser.save()
            messages.success(request, "Successfully Updated Profile")
            return HttpResponseRedirect(reverse("StaffEditProfile"))
        except:
            messages.error(request, "Failed to Update Profile")
            return HttpResponseRedirect(reverse("StaffEditProfile"))


def take_attendance(request):
    subjects = Subjects.objects.filter(staff_id=request.user.id)
    session_years = SessionYearModel.objects.all()
    params = {"subjects": subjects, "session_years": session_years}
    return render(request, "dashboard/staff_templates/staff_take_attendance.html", params)

# Here We are using Csrf Exempt Token because We are
# Not using any form submit our data.
def view_attendance(request):
    return render(request,'dashboard/staff_templates/staff_view_attendance.html')

def update_attendance(request):
    subjects = Subjects.objects.filter(staff_id=request.user.id)
    session_obj=SessionYearModel.objects.all()
    params={'subjects':subjects,'session_years':session_obj}
    return render(request,'dashboard/staff_templates/staff_update_attendance.html',params)

@csrf_exempt
def get_students(request):
    subject_id = request.POST.get('subject')
    session_year = request.POST.get('session_year')
    print('subkect:'+str(subject_id))
    print('session:'+str(session_year))
    subject = Subjects.objects.get(id=subject_id)
    session_model = SessionYearModel.objects.get(id=session_year)
    students = Students.objects.filter(course_id=subject.course_id, session_year_id=session_model)
    student_data=[]
    for student in students:
        small_data={'id':student.admin.id,"name":student.admin.first_name+" "+student.admin.last_name}
        student_data.append(small_data)
    return JsonResponse(json.dumps(student_data),content_type="application/json",safe=False)

@csrf_exempt
def save_attendance(request):
    print('save attendance')
    student_id=request.POST.get('student_ids')
    dict_student=json.loads(student_id)
    attendance_date=request.POST.get('attendance_date')
    subject_id=request.POST.get('subject_id')
    session_year=request.POST.get('session_year')
    subject_model=Subjects.objects.get(id=subject_id) 
    session_year_model=SessionYearModel.objects.get(id=session_year)
    try:
        attendance_model=Attendance(subject_id=subject_model,attendance_date=attendance_date,session_year_id=session_year_model)
        attendance_model.save()
        for item in dict_student:
            s_id=item['id'][:-2]
            student_model=Students.objects.get(admin=s_id)
            attendance_report=AttendanceReport(student_id=student_model,attendance_id=attendance_model,status=item['status'])
            attendance_report.save()
        return HttpResponse('Attendance Saved')
    except Exception as e:
        return HttpResponse(e)

@csrf_exempt
def get_attendance(request):
    subject_id=request.POST.get('subject_id')
    session_id=request.POST.get('session_year')
    attendance_record=Attendance.objects.filter(subject_id=str(subject_id),session_year_id=str(session_id))
    attendance_record_list=[]
    for attendance in attendance_record:
        data={
            'id':attendance.id,
            'attendance_date':str(attendance.attendance_date),
            'session_year_id':attendance.session_year_id.id
        }
        attendance_record_list.append(data)

    return JsonResponse(json.dumps(attendance_record_list),safe=False)

@csrf_exempt
def fetch_student(request):
    print('Fetch Student')
    attendance_date_id=request.POST.get('attendance_date_id')
    subject_id = request.POST.get('subject_id')
    session_year = request.POST.get('session_year')
    print('subkect:'+str(subject_id))
    print('session:'+str(session_year))
    subject = Subjects.objects.get(id=subject_id)
    session_model = SessionYearModel.objects.get(id=session_year)
    attendance_model=Attendance.objects.get(id=attendance_date_id)
    attendance_report=AttendanceReport.objects.filter(attendance_id=attendance_model)
    report_data_list=[]
    for student in attendance_report:
        small_data={'student_id':student.student_id.id,
        'admin_id':student.student_id.admin.id,
        "name":student.student_id.admin.first_name+" "+student.student_id.admin.last_name,
        'status':student.status
        }
        report_data_list.append(small_data)
    print(report_data_list)
    return JsonResponse(json.dumps(report_data_list),content_type="application/json",safe=False)


@csrf_exempt
def updated_attendance(request):
    print('Update attendance')
    student_ids=request.POST.get('student_ids')
    attendance_model_id=request.POST.get('attendance_model_id')
    # Converting JSON into Dictionary
    dict_student=json.loads(student_ids)
    try:
        for item in dict_student:
            s_id=item['id']
            student_model=Students.objects.get(id=s_id)
            attendance_model=Attendance.objects.get(id=str(attendance_model_id))
            attendance_report=AttendanceReport.objects.get(student_id=student_model,attendance_id=attendance_model)
            attendance_report.status=item['status']
            attendance_report.save()
        print('attendance report')
        return HttpResponse('Updated Attendance')
    except Exception as e:
        return HttpResponse(e)
    

def apply_leave(request):
    admin_obj=CustomUser.objects.get(id=request.user.id)
    staff_obj=Staffs.objects.get(admin=admin_obj)
    prev_leave_data=LeaveReportStaff.objects.filter(staff_id=staff_obj)
    param={
        'prev_leave_data':prev_leave_data
    }
    return render(request,'dashboard/staff_templates/staff_apply_leave.html',param)


def apply_leave_save(request):
    if request.method != "POST":
        return HttpResponse("Method not allowed")
    else:
        leave_date = request.POST.get('leave_date')
        leave_reason = request.POST.get('leave_reason')
        try:
            admin_obj=CustomUser.objects.get(id=request.user.id)
            staff_obj = Staffs.objects.get(admin=admin_obj)
            leave_report_obj=LeaveReportStaff(staff_id=staff_obj,leave_date=leave_date,leave_message=leave_reason)
            leave_report_obj.save()
            messages.success(request, "Succesfully Applied Leave Application")
            return HttpResponseRedirect(reverse('FacultyApplyLeave'))
        except Exception as e:
            messages.error(request, e)
            return HttpResponseRedirect(reverse('FacultyApplyLeave'))


def schedule_meeting(request):
    admin_obj=CustomUser.objects.get(id=request.user.id)
    staff_obj = Staffs.objects.get(admin=admin_obj)
    subjects=Subjects.objects.filter(staff_id=admin_obj)
    prev_schedule_meetings=ScheduleMeeting.objects.filter(staff_id=staff_obj)
    param={
        'prev_schedule_meetings':prev_schedule_meetings,
        'subjects':subjects
    }
    return render(request,'dashboard/staff_templates/staff_schedule_meeting.html',param)


def schedule_meeting_save(request):
    if request.method != "POST":
        return HttpResponse("Method not allowed")
    else:
        subject_id = request.POST.get('subject')
        topic = request.POST.get('topic')
        schedule_date = request.POST.get('date')
        schedule_time = request.POST.get('time')
        password = request.POST.get('password')
        meetingdetails = {
                        'host_email': 'ashutoshshrivastava00@gmail.com',
                        'schedule_for':'ashutoshshrivastava00@gmail.com',
                        "topic": str(topic),
                        "type": 2,
                        "start_time": f"{schedule_date}T{schedule_time}",
                        "duration": "45",
                        "timezone": "Asia/Calcutta",
                        "agenda": "test",
                        'password': str(password),
                        "recurrence": {"type": 1,
                                        "repeat_interval": 1
                                    },
                        "settings": {
                            "host_video": "true",
                            "participant_video": "true",
                            "join_before_host": "False",
                            "mute_upon_entry": "False",
                            "watermark": "true",
                            "audio": "voip",
                            "auto_recording": "cloud"
                            },
                        "registrants_email_notification": "true"
                        }
        try:
            create_meeting=createMeeting(meetingdetails)
            print(create_meeting['join_url'])
            print(create_meeting['password'])
            admin_obj=CustomUser.objects.get(id=request.user.id)
            staff_obj = Staffs.objects.get(admin=admin_obj)
            subject_obj=Subjects.objects.get(id=subject_id)
            schedule_meeting=ScheduleMeeting(topic_name=topic,staff_id=staff_obj,subject_id=subject_obj,
            start_url=create_meeting['start_url'],join_url=create_meeting['join_url'],meeting_password=create_meeting['password'],date=schedule_date,time=schedule_time)
            schedule_meeting.save()
            messages.success(request, "Succesfully Created Meeting")
            return HttpResponseRedirect(reverse('FacultyScheduleMeeting'))
        except Exception as e:
            messages.error(request, e)
            return HttpResponseRedirect(reverse('FacultyScheduleMeeting'))   


def feedback_menu(request):
    admin_obj=CustomUser.objects.get(id=request.user.id)
    staff_obj=Staffs.objects.get(admin=admin_obj)
    prev_feedback_data=FeedBackStaffs.objects.filter(staff_id=staff_obj)
    param={
        'feedbacks':prev_feedback_data
    }
    return render(request,'dashboard/staff_templates/staff_feedback_page.html',param)


def feedback_save(request):
    if request.method != "POST":
        return HttpResponse("Method not allowed")
    else:
        feedback_message = request.POST.get('feedback_message')
        try:
            admin_obj=CustomUser.objects.get(id=request.user.id)
            staff_obj = Staffs.objects.get(admin=admin_obj)
            feedback_obj=FeedBackStaffs(staff_id=staff_obj,feedback=feedback_message)
            feedback_obj.save()
            messages.success(request, "Feedsback Recieved")
            return HttpResponseRedirect(reverse('FacultyFeedbackMenu'))
        except Exception as e:
            messages.error(request, e)
            return HttpResponseRedirect(reverse('FacultyFeedbackMenu'))


def share_notes(request):
    admin_obj=CustomUser.objects.get(id=request.user.id)
    staff_obj = Staffs.objects.get(admin=admin_obj)
    subjects=Subjects.objects.filter(staff_id=admin_obj)
    prev_shared_notes=ShareNotes.objects.filter(staff_id=staff_obj)
    param={
        'prev_shared_notes':prev_shared_notes,
        'subjects':subjects
    }
    return render(request,'dashboard/staff_templates/staff_share_notes.html',param)


def share_notes_save(request):
    if request.method != "POST":
        return HttpResponse("Method not allowed")
    else:
        subject_id = request.POST.get('subject')
        staff_admin_id = request.user.id
        topic = request.POST.get('topic')
        print(topic)
        notes = request.FILES['notes']
        print(notes.name,notes.size)
        fs_obj = FileSystemStorage()
        filename = fs_obj.save(notes.name, notes)
        notes_url = fs_obj.url(filename)
        print(notes_url)
        try:
            admin_obj=CustomUser.objects.get(id=staff_admin_id)
            staff_obj = Staffs.objects.get(admin=admin_obj)
            subject_obj=Subjects.objects.get(id=subject_id)
            notes_obj=ShareNotes(topic=topic,subject_id=subject_obj,staff_id=staff_obj,notes=notes_url)
            notes_obj.save()
            messages.success(request, "Notes Succesfullt saved")
            return HttpResponseRedirect(reverse('FacultyShareNotes'))
        except Exception as e:
            messages.error(request, e)
            return HttpResponseRedirect(reverse('FacultyShareNotes'))
    


