from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class CaseInsensitiveModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        
        try:
            # Perform a case-insensitive lookup on the username field
            user = UserModel._default_manager.get(username__iexact=username)
        except UserModel.DoesNotExist:
            # Run the default password hasher once to prevent timing attacks
            UserModel().set_password(password)
        except UserModel.MultipleObjectsReturned:
            # Fallback to exact match if multiple users have same case-insensitive username
            try:
                user = UserModel._default_manager.get(username=username)
            except UserModel.DoesNotExist:
                return None
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        return None
