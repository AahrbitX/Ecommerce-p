# from django.contrib.auth import authenticate, login
# from common.utils import generate_token
# from common.models import CustomUser
 

# class UserHandler:

#     @staticmethod
#     def authenticate_user(mobile_number, password):
#         user = authenticate(mobile_number=mobile_number, password=password)
#         return user

#     @staticmethod
#     def generate_tokens(user):
#         access_token = generate_token(user)
#         return {
#             'access': access_token
#         }