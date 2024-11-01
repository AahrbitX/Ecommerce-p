from common.views import SignupView,LoginView,CurrentUserView
from django.urls import path
urlpatterns=[

    path('signup/',SignupView.as_view(),name='signup'),
    path('login/',LoginView.as_view(),name='login'),
     
     path('currentuser/', CurrentUserView.as_view(), name='current-user'),
]