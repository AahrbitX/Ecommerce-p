from common.models import *
from products.models import *
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from products.serializers import *
 
 
  
  # handlers.py

from django.core.exceptions import ObjectDoesNotExist
from .models import Product

class ProductHandler:
    
    @staticmethod
    def create_product(validated_data):
        category = validated_data.pop('category')
        product = Product.objects.create(**validated_data, category=category)
        return product

    @staticmethod
    def get_filtered_products(request):
        search_query = request.query_params.get('search', None)
        ordering = request.query_params.get('ordering', None)

        products = Product.objects.filter(status=True)
        
        if search_query:
            products = products.filter(name__icontains=search_query) | products.filter(description__icontains=search_query)

        if ordering:
            ordering_fields = ordering.split(',')
            valid_fields = ['price', '-price', 'rating', '-rating']
            ordering_fields = [field for field in ordering_fields if field in valid_fields]
            products = products.order_by(*ordering_fields)

        return products

    @staticmethod
    def delete_product(product_id):
        try:
            product = Product.objects.get(product_id=product_id)
            product.delete()
            return {"status": "SUCCESS", "message": "Product deleted successfully."}
        except ObjectDoesNotExist:
            raise ValueError("Product with the provided ID does not exist.")

    @staticmethod
    def update_product(product_id, update_data):
        try:
            product = Product.objects.get(product_id=product_id)
            
            if 'category' in update_data:
                category_id = update_data.pop('category')
                try:
                    category_instance = Category.objects.get(id=category_id)
                    update_data['category'] = category_instance
                except Category.DoesNotExist:
                    raise ValueError("Category with the provided ID does not exist.")
            
            for attr, value in update_data.items():
                setattr(product, attr, value)
            product.save()
            return product
        except ObjectDoesNotExist:
            raise ValueError("Product with the provided ID does not exist.")
