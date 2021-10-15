from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend 

#1 Django Default authentication works with Username and Password
#2.Since we are taking email(as the username),password we need to build our cutom authentication
#3.So that the user can authenticate itself
class EmailBackEnd(ModelBackend):
    def authenticate(self, username=None,password=None,**kwargs):
        UserModel=get_user_model()
        try:
            user=UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None

# 1 to authenticate first we inhereted the default class from the django modelsbackEnd.
# 2 afetr that we tried to get the user model through its email.
# 3 if the user was not present we came to the exception block and returned none.
# 4 else we checked the user for its password and returned the user if matched.




# Atlast we have to register our new overided backend model in the setting