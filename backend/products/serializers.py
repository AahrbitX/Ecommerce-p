from rest_framework import serializers
from backend.products.models import *
from backend.products.handlers import ProductHandler

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']
 
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image', 'uploaded_at']
class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    user=serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())  
    images = serializers.ListField(
      child=serializers.ImageField(), write_only=True, required=False)
    class Meta:
        model = Product
        fields = ['user','product_id', 'name', 'description', 'price', 'discount_price', 'category', 'rating', 'stock', 'images', 'status', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        handlers=ProductHandler()
        return handlers.create_product(validated_data)

class CartSerializer(serializers.ModelSerializer):
    total_price = serializers.ReadOnlyField()   

    class Meta:
        model = Cart
        fields = ['product_id', 'quantity', 'created_at', 'updated_at', 'total_price']

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id','street_address', 'city', 'state', 'postal_code', 'country', 'created_at']


    def validate_postal_code(self, value):
        """
        Validate the postal code if necessary (you can customize this).
        """
        if not value.isdigit():
            raise serializers.ValidationError("Postal code must be numeric.")
        return value
    

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=OrderItem
        fields='__all__'


class OrderSerializer(serializers.ModelSerializer):
    address = AddressSerializer()   
    order_items = OrderItemSerializer(many=True)   

    class Meta:
        model = Order
        fields = ['address',  'order_items',]