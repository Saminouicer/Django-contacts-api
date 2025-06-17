import jwt
from rest_framework import authentication , exceptions
from django.conf import settings
from django.contrib.auth.models import User




class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_data = authentication.get_authorization_header(request)

        if not auth_data:
            return None

        try:
            # Decode and safely split the token
            token_parts = auth_data.decode('utf-8').split()

            if len(token_parts) != 2 or token_parts[0].lower() != 'bearer':
                raise exceptions.AuthenticationFailed('Invalid token header. No Bearer keyword.')

            token = token_parts[1]

            # Decode JWT
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])

            # Get user
            user = User.objects.get(username=payload['username'])
            return (user, token)

        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token expired, login again.')
        except jwt.DecodeError:
            raise exceptions.AuthenticationFailed('Token is invalid, login again.')
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('User not found.')
        except Exception as e:
            raise exceptions.AuthenticationFailed(f'Authentication error: {str(e)}')
