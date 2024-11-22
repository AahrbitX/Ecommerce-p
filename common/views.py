from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 
from django.contrib.auth import authenticate
from common.serializers import *
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated,AllowAny
from common.handlers import CustomUserHandler, ResetPasswordHandler 
from rest_framework.exceptions import ValidationError


class SignupView(APIView):
    def post(self, request):
        try:
            user = CustomUserHandler.signup_user(request.data)
            return Response({"message": "User registered successfully", "user": user.user_id}, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        

class LoginView(APIView):
    def post(self, request):

        email=request.data.get('email')
        password = request.data.get('password')
        
        user = authenticate(request, email=email,password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                 
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

 
    
#user dashboard
class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

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
            return Response({"error": str(e)}, status=400)

class VerifyOtpView(APIView):
    def post(self, request):
        try:
            result = ResetPasswordHandler.verify_otp(request)
            return Response(result)
        except ValidationError as e:
            return Response({"error": str(e)}, status=400)