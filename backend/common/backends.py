from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken, TokenBackendError
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
import logging

logger = logging.getLogger('custom_logger')

class EmailBackend(BaseBackend):

    def authenticate(self, request,username=None, email=None, password=None, **kwargs):
        UserModel=get_user_model()

        try:
            user=UserModel.objects.get(email=email)

            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:

            return None

class TokenExpiredException(AuthenticationFailed):
    default_detail = "Your token has expired. Please refresh your token or login again."
    default_code = "token_expired"       

class CookieJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # Retrieve the token from cookies
        token = request.COOKIES.get('access_token')
        if not token:
            logger.warning("No token found in cookies for authentication.")
            return None  # Return `None` if no token is provided, allowing other authenticators to try.

        try:
            # Validate the JWT token
            validated_token = AccessToken(token)
            user_id = validated_token.get("user_id")

            # Fetch the user model dynamically
            UserModel = get_user_model()
            user = UserModel.objects.get(user_id=user_id)

            logger.info(f"Cookie Auth: User {user.email} (ID: {user.user_id}) authenticated successfully")

            return (user, None)  # Return authenticated user
        except TokenError as e:
            # if e.code == "token_not_valid" and "exp" in e.args[0].get("detail", {}):
            #     logger.warning("Token has expired.")
            #     raise TokenExpiredException()
            logger.error(f"Token validation error: {str(e)}")
            raise AuthenticationFailed("Invalid token.")
        except UserModel.DoesNotExist:
            logger.error(f"User with ID {user_id} not found.")
            raise AuthenticationFailed("User not found.")
        except Exception as e:
            logger.exception(f"Unexpected error during authentication: {str(e)}")
            raise AuthenticationFailed("Authentication failed due to an unexpected error.")