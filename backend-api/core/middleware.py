"""General web socket and non web socket middlewares"""

from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections
from jwt import decode as jwt_decode
# from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import UntypedToken
from urllib.parse import parse_qs

User = get_user_model()


@database_sync_to_async
def get_user(validated_token):
    try:
        user = User.objects.get(id=validated_token["user_id"])
        # return User.objects.get(id=token_id)
        print(user)
        return user
    except User.DoesNotExist:
        print("user doesn't exist")
        return AnonymousUser()


class JwtAuthMiddleware(BaseMiddleware):
    # Ses https://morioh.com/p/71b218237c9d and 
    # https://stackoverflow.com/questions/65297148/django-channels-jwt-authentication
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
       # Close old database connections to prevent usage of timed out connections
        close_old_connections()

        # Get the token
        try:
            token = parse_qs(scope["query_string"].decode("utf8"))["token"][0]
        except KeyError:
            scope['user'] = AnonymousUser()
        else:
            print(token)

            # Try to authenticate the user
            try:
                # This will automatically validate the token and raise an error if token is invalid
                UntypedToken(token)
            except (InvalidToken, TokenError) as e:
                # Token is invalid
                print(e)
                return None
            else:
                #  Then token is valid, decode it
                decoded_data = jwt_decode(token, settings.SECRET_KEY, algorithms=["HS256"])
                print(decoded_data)
                # Will return a dictionary like -
                # {
                #     "token_type": "access",
                #     "exp": 1568770772,
                #     "jti": "5c15e80d65b04c20ad34d77b6703251b",
                #     "user_id": 6
                # }

                # Get the user using ID
                scope["user"] = await get_user(validated_token=decoded_data)
        return await super().__call__(scope, receive, send)


def JwtAuthMiddlewareStack(inner):
    return JwtAuthMiddleware(AuthMiddlewareStack(inner))


