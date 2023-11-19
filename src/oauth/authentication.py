from datetime import datetime, timedelta
from django.conf import settings
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed
from .models import CustomUser
import jwt


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        if not token:
            return None
        token = self.get_the_token_from_header(token)

        try:
            payload = jwt.decode(token, settings.SECRET_JWT_KEY, algorithms=[settings.ALGORITHM])
        except jwt.exceptions.InvalidSignatureError:
            raise AuthenticationFailed('Invalid signature')
        except jwt.exceptions.DecodeError:
            raise AuthenticationFailed('Invalid token')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired')
        except Exception as e:
            return str(e)

        email = payload.get('email')
        if not email:
            raise AuthenticationFailed('User identifier not found in JWT')

        user = CustomUser.objects.get(email=email)

        if not user:
            raise AuthenticationFailed('User not found')

        return user, payload

    @classmethod
    def create_access(cls, user):
        payload = {
            'id': str(user.id),
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'exp': datetime.utcnow() + timedelta(days=10)
        }
        access_token = jwt.encode(payload, settings.SECRET_JWT_KEY, algorithm=settings.ALGORITHM)
        return access_token

    @classmethod
    def create_refresh(cls, user):
        payload = {
            'id': str(user.id),
            'exp': datetime.utcnow() + timedelta(minutes=15)
        }
        refresh_token = jwt.encode(payload, settings.SECRET_JWT_KEY, algorithm=settings.ALGORITHM)
        return refresh_token

    @classmethod
    def update_access_token(cls, refresh_token: str):
        try:
            payload = jwt.decode(refresh_token, settings.SECRET_JWT_KEY, algorithms=[settings.ALGORITHM])
        except jwt.exceptions.InvalidSignatureError:
            raise AuthenticationFailed('Invalid signature')
        except jwt.exceptions.DecodeError:
            raise AuthenticationFailed('Invalid token')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expire')

        user_id = payload.get('id')
        user = CustomUser.objects.get(id=user_id)

        if not user:
            raise AuthenticationFailed('User not found')

        new_access_token = cls.create_access(user)
        return new_access_token

    @classmethod
    def get_the_token_from_header(cls, token: str):
        token = token.replace('Bearer', '').replace(' ', '')
        return token
