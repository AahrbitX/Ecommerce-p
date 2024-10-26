from common.views import SignupView,Loginview,CurrentUserView
from django.urls import path
urlpatterns=[

    path('signup/',SignupView.as_view(),name='signup'),
    path('login/',Loginview.as_view(),name='login'),

    path('currentuser/',CurrentUserView.as_view(),name='currentuser')
]