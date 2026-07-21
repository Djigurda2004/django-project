from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import check_password
from .models import User

class EmailAuthBackend(ModelBackend):
    def authenticate(self,request,username=None,password=None):
        if '@' in username:
            try:
                user = User.objects.get(email=username)
                if user.check_password(password) and user.is_active:
                    return user
            except User.DoesNotExist:
                pass
        return None