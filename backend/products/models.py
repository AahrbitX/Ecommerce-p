from django.db import models
import uuid
from common.models import CustomUser

class DateAbstract(models.Model):
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    
    class Meta:
        abstract = True

    
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
   
    
class Product(DateAbstract):

    ENABLE = 1
    DISABLE = 0
    DELETED = 2
    STATUS_OPTIONS = (
        (ENABLE, 'active'),
        (DISABLE, 'inactive'),
        (DELETED, 'deleted')
    )
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True,blank=True)
    product_id = models.UUIDField(default=uuid.uuid4,primary_key=True, editable=False, unique=True)  
    name = models.CharField(max_length=255)
    description = models.TextField(null=True,blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    rating = models.FloatField(default=0,null=True ,help_text="Product rating out of 5")
    stock = models.PositiveIntegerField(default=0, help_text="Number of items available in stock")
    # image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    status = models.BooleanField(default=ENABLE,choices=STATUS_OPTIONS)
     
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['name', 'category']),
        ]
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return f"{self.name}  {self.product_id}"

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/', null=True, blank= True)
    uploaded_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return str(self.image)

class Cart(models.Model):

    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)   
    updated_at = models.DateTimeField(auto_now=True)   

    def __str__(self):
        return f"{self.user} - {self.product} (Qty: {self.quantity})"

    @property
    def total_price(self):
       
        return self.quantity * self.product.discount_price

class Address(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="addresses")
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Address of {self.user.email}"

class Order(models.Model):
    order_id=models.UUIDField(primary_key=True,default = uuid.uuid4)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    ordered_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ("Pending", "Pending"),
        ("Shipped", "Shipped"),
        ("Delivered", "Delivered"),
        ("Cancelled", "Cancelled"),
    ], default="Pending")

    def __str__(self):
        return f"Order {self.order_id} by {self.user.email}"

 
class OrderItem(models.Model):
    order_item_id=models.UUIDField(primary_key=True,default = uuid.uuid4)
    order_items= models.ForeignKey(Order, related_name="order_items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} x {self.quantity} for Order {self.order_item_id}"
    



class Payment(models.Model):

    PAYMENT_STATUS=[
        ("Pending", "Pending"),
        ("Completed", "Completed"),
        ("Failed", "Failed")
        ]
    
    PAYMENT_METHOD=[
        ("Credit Card", "Credit Card"),
        ("Debit Card", "Debit Card"),
        ("PayPal", "PayPal"),
        ("Bank Transfer", "Bank Transfer"),
    ]
    
    order = models.ForeignKey(Order, related_name="payments", on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50,choices=PAYMENT_METHOD)
    status_status = models.CharField(max_length=20, choices=PAYMENT_STATUS,default="Pending")

    def __str__(self):
        return f"Payment {self.id} for Order {self.order.id}"
