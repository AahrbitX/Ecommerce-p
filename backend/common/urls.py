from common.views import SignupView, LoginView,DashboardView, ForgotPasswordView, VerifyOtpView, Logout, UserProfileView
from django.urls import path
urlpatterns=[

    path('signup/',SignupView.as_view(),name='signup'),
    path('login/',LoginView.as_view(),name='login'),
    path('logout/', Logout.as_view(),name='logout'),
    path('currentuser/', DashboardView.as_view(), name='current-user'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('verify-otp/', VerifyOtpView.as_view(), name='verify_otp'),
    path('user-profile/', UserProfileView.as_view(), name='edit_profile'),
]