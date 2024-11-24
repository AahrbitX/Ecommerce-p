from django.db.models.signals import post_delete
from django.dispatch import receiver
import os
from django.conf import settings
from .models import Product

@receiver(post_delete, sender=Product)
def delete_product_image(sender, instance, **kwargs):
    
    if instance.image:
        image_path = instance.image.path
        if os.path.isfile(image_path):
            os.remove(image_path)