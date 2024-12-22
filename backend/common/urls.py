from common.views import SignupView, LoginView,DashboardView, ForgotPasswordView, VerifyOtpView, Logout, UserProfileView, \
                          VendorApplicationCreateView, ApproveVendorApplicationView, RejectVendorApplicationView
from django.urls import path
urlpatterns=[

    path('signup/',SignupView.as_view(),name='signup'),
    path('login/',LoginView.as_view(),name='login'),
    path('logout/', Logout.as_view(),name='logout'),
    path('currentuser/', DashboardView.as_view(), name='current-user'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('verify-otp/', VerifyOtpView.as_view(), name='verify_otp'),
    path('user-profile/', UserProfileView.as_view(), name='edit_profile'),
    
    path('vendor/application/', VendorApplicationCreateView.as_view(), name='vendor-application-create'),
    path('vendor/application/approve/<uuid:application_id>/', ApproveVendorApplicationView.as_view(), name='approve-vendor-application'),
    path('vendor/application/reject/<uuid:application_id>/', RejectVendorApplicationView.as_view(), name='reject-vendor-application')

]