from rest_framework import serializers
from products.models import *
from products.handlers import ProductHandler




class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']
 
class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    
    
    class Meta:
        model = Product
        fields = ['product_id', 'name', 'description', 'price', 'discount_price', 'category', 'rating', 'stock', 'image', 'status', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        
        
        handlers=ProductHandler()

        return handlers.create_product(validated_data)

class CartSerializer(serializers.ModelSerializer):
    total_price = serializers.ReadOnlyField()   

    class Meta:
        model = Cart
        fields = ['product_id', 'quantity', 'created_at', 'updated_at', 'total_price']

 