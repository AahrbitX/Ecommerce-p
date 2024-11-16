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

    product_id = models.UUIDField(default=uuid.uuid4,primary_key=True, editable=False, unique=True)  
    name = models.CharField(max_length=255)
    description = models.TextField(null=True,blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    rating = models.FloatField(default=0,null=True ,help_text="Product rating out of 5")
    stock = models.PositiveIntegerField(default=0, help_text="Number of items available in stock")
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    status = models.BooleanField(default=ENABLE,choices=STATUS_OPTIONS)
     
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['name', 'category']),
        ]
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.name
    

class Cart(models.Model):

    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)   
    updated_at = models.DateTimeField(auto_now=True)   

    def __str__(self):
        return f"{self.user} - {self.product} (Qty: {self.quantity})"

    @property
    def total_price(self):
       
        return self.quantity * self.product.discount_price


