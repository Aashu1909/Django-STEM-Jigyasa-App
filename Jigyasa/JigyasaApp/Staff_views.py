from django.http.response import HttpResponse,JsonResponse
from django.shortcuts import render
from .models import SessionYearModel, Subjects, Students, Attendance,AttendanceReport
from django.views.decorators.csrf import csrf_exempt
import json


def faculty_home(request):
    return render(request, 'dashboard/staff_templates/home_content.html')

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
    