from common.views import SignupView,LoginView,CurrentUserView, ForgotPasswordView, VerifyOtpView
from django.urls import path
urlpatterns=[

    path('signup/',SignupView.as_view(),name='signup'),
    path('login/',LoginView.as_view(),name='login'),
     
     path('currentuser/', CurrentUserView.as_view(), name='current-user'),

    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('verify-otp/', VerifyOtpView.as_view(), name='verify_otp'),
]