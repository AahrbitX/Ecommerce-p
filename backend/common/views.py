from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 
from django.contrib.auth import authenticate
from common.serializers import *
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated,AllowAny
from common.handlers import CustomUserHandler, ResetPasswordHandler 
from rest_framework.exceptions import ValidationError
from common.backends import CookieJWTAuthentication

class SignupView(APIView):
    def post(self, request):
        try:
            user = CustomUserHandler.signup_user(request.data)
            return Response({"message": "User registered successfully", "user": user.user_id}, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
class Logout(APIView):
    def post(self, request):
        response = Response({"detail": "Successfully logged out"}, status=status.HTTP_200_OK)
        response.delete_cookie('access_token')  

        return response
class LoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        user = authenticate(request, email=email, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            response = Response({
                'access': str(refresh.access_token), 
                "message": "Successfuly logged"
            }, status=status.HTTP_200_OK)
            response.set_cookie(
                key='access_token',
                value=str(refresh.access_token),
                httponly=True,      # Prevent JavaScript access
                # secure=True,       # Use True in production (HTTPS)
                # samesite='Lax',    # Adjust if cross-origin requests are needed
                max_age=50000,       # Expiry in seconds
            )
            return response
        
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
    
#user dashboard
class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]

    def get(self, request):
        user = request.user  
        return Response({
            'user_id': str(user.user_id), 
            'email': user.email,
        })
    

class ForgotPasswordView(APIView):
    def post(self, request):
        try:
            result = ResetPasswordHandler.forgot_password(request)
            return Response({"message": "OTP has been sent successfully"},status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class VerifyOtpView(APIView):
    def post(self, request):
        try:
            result = ResetPasswordHandler.verify_otp(request)
            return Response(result)
        except ValidationError as e:
            return Response({"error": str(e)}, status=400)