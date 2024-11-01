from django.shortcuts import render,get_object_or_404
from rest_framework.views import APIView
from rest_framework import generics
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from products.models import Product
from products.handlers import ProductHandler
 

"""code follows structured pattern kindly retrack to understand"""
class ProductAPIView(APIView):
    
    def get(self, request, product_id=None):
        if product_id:
            product = get_object_or_404(Product, product_id=product_id)
            serializer = ProductSerializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK)

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

    def patch(self, request, product_id):
        try:
            updated_product = ProductHandler.update_product(product_id, request.data)
            return Response({"status": "SUCCESS"}, status=status.HTTP_200_OK)
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