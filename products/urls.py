# urls.py
from django.urls import path
from products.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
     # path('signup/', SignupAPIView.as_view(), name='signup'),
     # path('login/', LoginAPIView.as_view(), name='login'),
     
     path('create/', ProductCreateAPIView.as_view(), name='product-create-list'),
      
     path('createm/', product_form, name='create_product'),
     
     path('products/<int:product_id>/', ProductCreateAPIView.as_view(), name='product-detail'),
]

if settings.DEBUG:  

 urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
