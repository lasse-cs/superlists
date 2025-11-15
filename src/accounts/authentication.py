from accounts.models import Token, User


class PasswordlessAuthenticationBackend:
    def authenticate(self, request, uid):
        try:
            token = Token.objects.get(uid=uid)
        except Token.DoesNotExist:
            return None
        user, _ = User.objects.get_or_create(email=token.email)
        return user

    def get_user(self, email):
        return User.objects.filter(email=email).first()
