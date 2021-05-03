from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class TokenManager:
    """
    Provides JWT access token to verified users.
    Verified user = Old user registering again with correct password 
    due to token expire, or, Newly registered user
    """
    def __init__(self, username, password):
        self._user = self._user_exists(username)
        self._user_verified = False

        if self._user is not None:
            self._verify_password(password)
        else:
            self._user = self._create_user(username, password)
            self._user_verified = True

    def get_access_token(self):
        if not self._user_verified:
            raise Exception('User not verified')
        return RefreshToken.for_user(self._user).access_token

    def _create_user(self, username, password):
        user = User(username=username)
        user.set_password(password)
        user.save()
        return user

    def _user_exists(self, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None
        
        return user

    def _verify_password(self, password):
        if self._user.check_password(password):
            self._user_verified = True
