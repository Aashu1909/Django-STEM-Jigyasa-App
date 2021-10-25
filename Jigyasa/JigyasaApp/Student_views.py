from django.shortcuts import render


def student_home(request):
    return render(request, 'dashboard/student_templates/home_content.html')