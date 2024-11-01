# urls.py
from django.urls import path
from products.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
     
       path('products/', ProductAPIView.as_view(), name='product-list'),
      
       path('products/<uuid:product_id>/', ProductAPIView.as_view(), name='product-detail'),

       path('categories/', CategoryView.as_view(), name='category'),

       path('categories/<int:pk>/', CategoryView.as_view(), name='category-detail'),
]

if settings.DEBUG:  

 urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
