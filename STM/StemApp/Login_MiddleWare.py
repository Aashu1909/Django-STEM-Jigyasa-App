from django.http.response import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin
from django.urls import reverse

# Login middleware function provides us the ability to Set the views of the user.
# like Student cannot access admin urls and admin and staff cannot do the same or vice versa.
# For This thing we have to create a custom Middleware
# Middleware is a framework of hooks into Django request/response processing
# In simple words when a user request (Acces URL endpoint) then first it will come to the middleware
# then the futher request is procesed.

class LoginCheckMiddleWare(MiddlewareMixin):
    def process_view(self,request,view_function,view_arg,view_kwargs):
        modulename=view_function.__module__
        user=request.user
        if user.is_authenticated:
            if user.user_type == '1':
                print('user type :1')
                if modulename == 'StemApp.Admin_views':
                    print('Admin_views')
                    pass
                elif modulename == 'StemApp.views' or modulename == "django.views.static":
                    print('Views-Hod ')
                    pass
                else:
                    print('redirect to Admin Home')
                    return HttpResponseRedirect(reverse('AdminHome'))
            elif user.user_type == '2':
                print('user type :2')
                print(user.first_name)
                print(user.id)
                if modulename == 'StemApp.Staff_views' or modulename == "django.views.static":
                    print('staffviews&Static')
                    pass
                elif  modulename == 'StemApp.views':
                    print('views->for->staff')
                    pass
                else:
                    return HttpResponseRedirect(reverse('FacultyHome'))
            elif user.user_type == '3':
                print('user type :3')
                if modulename == 'StemApp.Student_views' or modulename == "django.views.static":
                    print('studentviews')
                    pass
                elif modulename == 'StemApp.views':
                    print('views->for->student')
                    pass
                else:
                    return HttpResponseRedirect(reverse('StudentHome'))
        else:
            print('userNot authenticated')           
            if request.path == reverse('ShowLogin') or request.path == reverse('doLogin') or request.path == reverse('homePage') or modulename == "django.contrib.auth.urls":
                print('pass:->login or showlogin or homepage or modulename= django.contrib.auth.urls')
                pass
            else:
                if request.path == reverse('ShowLogin'):
                    print('redirect to Show Login')
                    return HttpResponseRedirect(reverse('ShowLogin'))
                if request.path == reverse('doLogin'):
                    print('do login:redirect to show Login')
                    return HttpResponseRedirect(reverse('ShowLogin'))
                if request.path == reverse('homePage'):
                    print('redirect to home Login')
                    return HttpResponseRedirect(reverse('ShowLogin'))

# So basically this logic will restrict User to access page that is not allowed by its user types 
# ie student cannot access HOD,staff