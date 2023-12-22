import jwt
from datetime import datetime, timedelta
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
def generate_jwt_token(user):
    payload = {
        'user_id': user.id,
        'user_role_id': user.user_role.role_id,
        'exp': datetime.utcnow() + timedelta(days=1),  # Token expiration time (adjust as needed)
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')


class CustomRefreshToken(RefreshToken):
    @classmethod
    def for_user(cls, user):
        token = super().for_user(user)
        # Add the 'role_id' to the token claims
        token['role_id'] = user.user_role.role_id
        return token