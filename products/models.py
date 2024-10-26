from django.db import models
import uuid


class DateAbstract(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
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

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  
    name = models.CharField(max_length=255)
    description = models.TextField()
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
