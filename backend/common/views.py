from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 
from django.contrib.auth import authenticate
from common.serializers import *
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated,AllowAny
from common.handlers import CustomUserHandler, ResetPasswordHandler, VendorApplicationHandler
from rest_framework.exceptions import ValidationError
from common.backends import CookieJWTAuthentication
from rest_framework.permissions import IsAdminUser
from django.shortcuts import get_object_or_404
import logging

logger = logging.getLogger(__name__)


class SignupView(APIView):
    def post(self, request):
        try:
            user = CustomUserHandler.signup_user(request.data)
            return Response({"message": "User registered successfully", "user": user.user_id}, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
 
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

class Logout(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]
    def post(self, request):
        response = Response({"detail": "Successfully logged out"}, status=status.HTTP_200_OK)
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')   
        return response


#user dashboard
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]
    
    def post(self, request):
        user = request.user
        if hasattr(user, 'userprofile'):
            return Response({"detail": "Profile already exists."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            profile = serializer.save(user=user)
            return Response(UserProfileSerializer(profile).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request):
        user = request.user
        try:
            profile = user.userprofile
        except UserProfile.DoesNotExist:
            return Response({"detail": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)
        # user_serializer = CustomUser(user, partial = True)
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():#and user_serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DashboardView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]

    def get(self, request):
        user = request.user   
        if user:
            try:
                userprofile = UserProfile.objects.get(user=user)
            except UserProfile.DoesNotExist:
                userprofile = None
            return Response({
                'user_id': str(user.user_id),
                'email': user.email,
                'username': userprofile.name if userprofile and userprofile.name else "",
                'Contact Number': userprofile.phone_number if userprofile and userprofile.phone_number else "",
                'Bio': userprofile.bio if userprofile and userprofile.bio else "",
                'Profile Picture': userprofile.profile_picture.url if userprofile and userprofile.profile_picture else "",
            })
        return Response({"detail": "User not authenticated"}, status=401)
    

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

class VendorApplicationCreateView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        user = request.user
        try:
            handler = VendorApplicationHandler(data=data)
            detail_message, application_id = handler.create_vendor_application(user=request.user)
            return Response(
                {"detail": detail_message, "application_id": application_id}, 
                status=status.HTTP_201_CREATED
            )
        except ValidationError as e:
            return Response({"detail": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

    def get(self, request):
        try:
            store_id = request.query_params.get('store_id')
            if not store_id:
                return Response(
                    {
                        'data': "nothin",
                        'status': status.HTTP_201_CREATED,
                        'error': "store_id is required",
                    
                    },status=status.HTTP_201_CREATED    
                )
            store = get_object_or_404(VendorStore, store_id=store_id)
            serializer = VendorStoreSerializer(store)
            return Response(
                    {
                        'data': serializer.data,
                        'status': status.HTTP_200_OK,
                        'message': "success"
                    },
                    status=status.HTTP_200_OK
                )
        except Exception as e:
            logger.exception(f"Exception in RetrieveStoreDetails: error: {e}")
            return Response(
                {
                    'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'message': "Internal Server Error",
                    'data': {}
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            ) 

        
class ApproveVendorApplicationView(APIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [CookieJWTAuthentication]

    def post(self, request, application_id):
        try:
            application = VendorApplication.objects.get(vendor_application_id=application_id)
            handler = VendorApplicationHandler(application=application)
            detail_message = handler.approve_application()
            return Response(
                {"detail": detail_message, "message": "Your Application is Approved"}, 
                status=status.HTTP_200_OK
            )
        except VendorApplication.DoesNotExist:
            return Response({"detail": "Application not found."}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            return Response({"detail": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class RejectVendorApplicationView(APIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [CookieJWTAuthentication]

    def post(self, request, application_id):
        try:
            application = VendorApplication.objects.get(vendor_application_id=application_id)
            handler = VendorApplicationHandler(application=application)
            rejection_reason = request.data.get('rejection_reason')
            detail_message = handler.reject_application(rejection_reason)
            return Response(
                {"detail": detail_message, "message": "Your Application is Rejected"}, 
                status=status.HTTP_200_OK
            )
        except VendorApplication.DoesNotExist:
            return Response({"detail": "Application not found."}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            return Response({"detail": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)