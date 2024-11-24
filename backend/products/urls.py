# urls.py
from django.urls import path
from backend.products.views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
     
       path('products/', ProductAPIView.as_view(), name='product-list'),
      
       path('products/<uuid:product_id>/', ProductAPIView.as_view(), name='product-detail'),

       path('categories/', CategoryView.as_view(), name='category'),

       path('categories/<int:pk>/', CategoryView.as_view(), name='category-detail'),

       path('cart/', CartView.as_view(), name='cart-add'),

       path('address/<int:address_id>/', AddressCreateView.as_view(), name='address-detail'),
       path('address/', AddressCreateView.as_view(), name='address-create'),

       path('order/',OrderCreateView.as_view(),name='order') 

]

if settings.DEBUG:  

 urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
