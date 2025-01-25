from common.models import *
from products.models import *
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from products.serializers import *
from django.db import transaction

class ProductHandler:
    def __init__(self, validated_data):
        """
        Initialize the ProductHandler with the validated data.
        """
        self.validated_data = validated_data
        self.user = None
        self.category = None
        self.images = []

    def extract_data(self):
        """
        Extract and validate user, category, and images from validated data.
        """
        self.user = self.validated_data.pop('user', None)
        self.category = self.validated_data.pop('category', None)
        self.images = self.validated_data.pop('images', [])

        if not self.user:
            raise ValueError("User is required to create a product.")
        if not self.category:
            raise ValueError("Category is required to create a product.")

    def create_product(self):
        """
        Create a product and save associated images.
        """
        try:
            # Extract necessary fields
            self.extract_data()

            # Create the product
            product = Product.objects.create(
                **self.validated_data, user=self.user, category=self.category
            )

            # Save images if provided
            self._save_images(product)

            # Prepare response data
            response_data = {
                'product_id': product.product_id,
                'name': product.name,
                'description': product.description,
                'price': product.price,
                'discount_price': product.discount_price,
                'category': product.category.id,
                'rating': product.rating,
                'stock': product.stock,
                'status': product.status,
                'created_at': product.created_at,
                'updated_at': product.updated_at,
                'images': [img.image.url for img in product.images.all()],
            }

            return response_data
        except Exception as e:
            raise Exception(f"An error occurred while creating the product: {e}")

    def _save_images(self, product):
        """
        Private method to handle saving images associated with a product.
        """
        for image in self.images:
            ProductImage.objects.create(product=product, image=image)

      
          

    @staticmethod
    def get_filtered_products(request):
        search_query = request.query_params.get('search', None)
        ordering = request.query_params.get('ordering', None)
        category_id = request.query_params.get('category', None)
        min_price = request.query_params.get('min_price', None)
        max_price = request.query_params.get('max_price', None) 

        products = Product.objects.filter(status=True)
        if min_price:
          products = products.filter(price__gte=min_price)
        if max_price:
          products = products.filter(price__lte=max_price)

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

            category = update_data.pop('category', None)
            user = update_data.pop('user', None)
            images = update_data.pop('images', None)

            if 'category' in update_data:
                try:
                    category_instance = Category.objects.get(id=category)
                    product.category = category_instance
                except Category.DoesNotExist:
                    raise ValueError("Category with the provided ID does not exist.")
            if user:
                try:
                    user_instance = CustomUser.objects.get(user_id=user)
                    product.user = user_instance
                except CustomUser.DoesNotExist:
                    raise ValueError("User with the provided ID does not exist.")
                
            for attr, value in update_data.items():
                setattr(product, attr, value)

            product.save()   

            if images is not None:
                product.images.all().delete()
                for image in images:
                    ProductImage.objects.create(product=product, image=image)

            response_data = {
                'product_id': product.product_id,
                'name': product.name,
                'description': product.description,
                'price': product.price,
                'discount_price': product.discount_price,
                'category': product.category.id if product.category else None,
                'rating': product.rating,
                'stock': product.stock,
                'status': product.status,
                'created_at': product.created_at,
                'updated_at': product.updated_at,
                'images': [image.image.url for image in product.images.all()],
            }

            return response_data

        except Product.DoesNotExist:
            raise ValueError("Product with the provided ID does not exist.")
        except Exception as e:
            raise Exception(f"An error occurred while updating the product: {e}")


class CartHandler:
    
    @staticmethod
    def add_cart(request):

        user_id=request.data.get('user_id')
        
        user=get_object_or_404(CustomUser,user_id=user_id)
        product_id=request.data.get('product_id')
        product=get_object_or_404(Product,product_id=product_id)
        
        quantity=request.data.get("quantity")
        cart_item, created = Cart.objects.get_or_create(user=user,product=product)
        
        
        if not created:
          cart_item.quantity += int(quantity)
        else:
            cart_item.quantity = quantity
        cart_item.save()
        
        response = {
                "status": "SUCCESS",
               
                "data": {
                    "cart_id": cart_item.id,
                    "product_id": cart_item.product.product_id,
                    "product_name": cart_item.product.name,
                    "quantity": cart_item.quantity,
                    "user_id": cart_item.user.user_id
                }
            }
        return response
class AddressHandler:

    @staticmethod
    def create_address(validated_data, user):
        """
        Handles the creation of an Address object.
        """
        street_address = validated_data.pop('street_address')
        city = validated_data.pop('city')
        state = validated_data.pop('state')
        postal_code = validated_data.pop('postal_code')
        country = validated_data.pop('country')

       
        address = Address.objects.create(
            street_address=street_address,
            city=city,
            state=state,
            postal_code=postal_code,
            country=country,
            user=user   
        )
        
        return address


    @staticmethod
    def update_address(address_id, validated_data, user):
       
      try:
          address = Address.objects.get(id=address_id, user=user)
      except Address.DoesNotExist:
          raise ValueError("Address not found or doesn't belong to the user.")

         
      address.street_address = validated_data.get('street_address', address.street_address)
      address.city = validated_data.get('city', address.city)
      address.state = validated_data.get('state', address.state)
      address.postal_code = validated_data.get('postal_code', address.postal_code)
      address.country = validated_data.get('country', address.country)
  
      address.save()
      return address

    @staticmethod
    def delete_address(address_id, user):
        """
        Delete an address for the user.
        """
        try:
            address = Address.objects.get(id=address_id, user=user)
        except Address.DoesNotExist:
            raise ValueError("Address not found or doesn't belong to the user.")
        
        address.delete()
        return True

    @staticmethod
    def get_address(address_id, user):
        """
        Retrieve a specific address by its ID for the user.
        """
        try:
            address = Address.objects.get(id=address_id, user=user)
            return address
        except Address.DoesNotExist:
            raise ValueError("Address not found or doesn't belong to the user.")
  
 
class WishlistHandler:
    def __init__(self, product=None, user=None):
        self.product = product
        self.user = user

    def add_to_wishlist(self):

        wishlist_item, created = Wishlist.objects.get_or_create(user=self.user, product=self.product)
        return wishlist_item, created
    
    def remove_from_wishlist(self):
        try:
            wishlist_item = Wishlist.objects.get(user=self.user, product=self.product)
            wishlist_item.delete()
            return True
        except Wishlist.DoesNotExist:
            return False
    
    def get_wishlist(self):
        return Wishlist.objects.filter(user=self.user)

# Order handler
class OrderHandler:

  @staticmethod
  def create_order(request):
    try:
        with transaction.atomic():
           
            cart_items = Cart.objects.filter(user=request.user)
            if not cart_items.exists():
                raise ValueError("No items in the cart to create an order.")

            address_id = request.data.get("address_id")
            if not address_id:
                raise ValueError("Address ID is required to place an order.")
            
            try:
                address = Address.objects.get(id=address_id, user=request.user)
            except Address.DoesNotExist:
                raise ValueError("The provided address does not exist.")
            
            order = Order.objects.create(user=request.user, address=address)

            for cart_item in cart_items:
                OrderItem.objects.create(
                    order_items=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    total_price=cart_item.total_price,
                )

            cart_items.delete()

        return order
    except Exception as e:
       
        raise ValueError(f"An error occurred while creating the order: {str(e)}")

