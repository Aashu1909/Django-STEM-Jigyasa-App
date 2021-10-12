from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend 
#1 Django Default authentication works with Username and Password
#2.Since we are taking email(as the username),password we need to build our cutom authentication
#3.So that the user can authenticate itself
class EmailBackEnd(ModelBackend):
    def authenticate(self, username=None,password=None,*kwargs):
        UserModel=get_user_model()
        try:
            user=UserModel

