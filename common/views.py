from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 
from django.contrib.auth import authenticate
from common.serializers import *
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import default_token_generator
from rest_framework.permissions import IsAuthenticated,AllowAny
from common.utils import get_tokens_for_user

class SignupView(APIView):

    def post(self,request,*args,**kwargs):

        serializer=UserSerializer(data=request.data)

        if serializer.is_valid():
            
            user = serializer.save()
            tokens = get_tokens_for_user(user)

            
             
            return Response({
                'access': tokens,
                'username':user.username,
                'user_id': str(user.user_id)
            }, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)
    

class Loginview(APIView):
    def post(self, request, *args, **kwargs):
        
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            
            mobile_number = serializer.validated_data['mobile_number']
            password = serializer.validated_data['password']

            
            user = authenticate(request, mobile_number=mobile_number, password=password)

            if user is not None:
                refresh = RefreshToken.for_user(user)
                return Response({
                    # 'refresh': str(refresh),
                    'username':user.username,
                    'Mobile':user.mobile_number,
                    'access': str(refresh.access_token),
                    'status': 'Verified User',
                }, status=status.HTTP_200_OK)
                
        return Response({'detail': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'user_id': str(user.user_id),
            'username': user.username,
            'mobile_number': user.mobile_number,
        })