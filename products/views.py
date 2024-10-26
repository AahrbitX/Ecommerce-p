from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render

"""code follows structured pattern kindly retrack to understand"""

# class SignupAPIView(APIView):

#     def post(self, request, *args, **kwargs):
#         serializer = UserSignupSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()  # The handler is called here via the serializer
#             return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class LoginAPIView(APIView):

#     def post(self, request, *args, **kwargs):
       
#         handler = UserHandler()
#         try:
#             token = handler.login_user(request)
#             return Response({"token": token.key}, status=status.HTTP_200_OK)
#         except ValueError as e:
#             return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)   
 

class ProductCreateAPIView(APIView):
    
    def post(self, request, *args, **kwargs):
        print("Incoming data:", request.data) 
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.save()
            return Response(
                {"id": product.id, "message": "Product created successfully!"},
                status=status.HTTP_201_CREATED
            )
        
        return Response(
            {"errors": serializer.errors, "message": "Product creation failed."},
            status=status.HTTP_400_BAD_REQUEST
        )
    
     
    def get(self, request):
        
        
        products = ProductHandler.get_filtered_products(request)
        
        serializer = ProductSerializer(products, many=True)

        return Response (
            {'Data:':serializer.data}, status=status.HTTP_200_OK)
    



    def delete(self, request, product_id):
       
        handler = ProductHandler()
        try:
            result = ProductHandler.delete_product(product_id)
            return Response(result, status=status.HTTP_204_NO_CONTENT)

        except ValueError as e:
            return Response(
                {"status": "FAILURE", "error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        
    def patch(self, request, product_id):
         
        handler = ProductHandler()
        try:
            
            updated_product = handler.update_product(product_id, request.data)
            return Response({
                "status": "SUCCESS"},status=status.HTTP_200_OK)

        except ValueError as e:
            return Response({"status": "FAILURE", "error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        




def product_form(request):
     
    categories = Category.objects.all()
    
    
    return render(request, 'product.html', {'categories': categories})