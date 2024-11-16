from django.shortcuts import render,get_object_or_404
from rest_framework.views import APIView
from rest_framework import generics
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from products.models import Product
from products.handlers import ProductHandler,CartHandler
from rest_framework.permissions import IsAuthenticated

 

"""code follows structured pattern kindly retrack to understand"""
class ProductAPIView(APIView):
    
    def get(self, request, product_id=None):
        if product_id:
            product = get_object_or_404(Product, product_id=product_id)
            serializer = ProductSerializer(product)
            return Response(
                {"data":serializer.data},status=status.HTTP_200_OK)

        products = ProductHandler.get_filtered_products(request)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            product = ProductHandler.create_product(serializer.validated_data)
            return Response(
                {"data": product.product_id, "message": "Product created successfully!"},
                status=status.HTTP_201_CREATED
            )
        return Response(
            {"errors": serializer.errors, "message": "Product creation failed."},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    def delete(self, request, product_id):
        try:
            result = ProductHandler.delete_product(product_id)
            return Response(result, status=status.HTTP_204_NO_CONTENT)
        except ValueError as e:
            return Response(
                {"status": "FAILURE", "error": str(e)}, status=status.HTTP_404_NOT_FOUND
            )

    def patch(self, request, product_id=None):
        try:
            if product_id:

             updated_product = ProductHandler.update_product(product_id, request.data)
             return Response({"status": "SUCCESS","data":updated_product.product_id}, status=status.HTTP_200_OK)
            
            else:
                return Response("small error")
        except ValueError as e:
            return Response(
                {"status": "FAILURE", "error": str(e)}, status=status.HTTP_404_NOT_FOUND
            )

class CategoryView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CartView(APIView):
  
   def post(self,request,*args,**kwargs):
       permission_classes = [IsAuthenticated]

       
       result=CartHandler.add_cart(request)
       if result["status"] == "SUCCESS":
            return Response(
                {"data":result,"message":"Item added successfully"}, status=status.HTTP_200_OK)
       
       return Response(result, status=status.HTTP_400_BAD_REQUEST)
       
   def get(self, request): 
     permission_classes = [IsAuthenticated]
     
     user=request.user
      
     if user:
        
        cart_items = Cart.objects.filter(user=user)
        serializer = CartSerializer(cart_items, many=True)

        total_price = sum(item.total_price for item in cart_items)
        
        return Response({'data': serializer.data,
                         'Total_price':total_price}, status=status.HTTP_200_OK)
     else:
        
        return Response(

            {'error': 'User ID is required to retrieve cart items.'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
     
   def delete(self, request, *args, **kwargs):
        cart_id = request.data.get("cart_id")
        
        if not cart_id:
            return Response(
                {'error': 'Item ID is required to remove an item from the cart.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
           
            cart_item = Cart.objects.get(id=cart_id, user=request.user)
            cart_item.delete()
            return Response(
                {'message': 'Item removed from cart successfully'},
                status=status.HTTP_200_OK
            )
        except Cart.DoesNotExist:
            return Response(
                {'error': 'Item not found in your cart.'},
                status=status.HTTP_404_NOT_FOUND
            )