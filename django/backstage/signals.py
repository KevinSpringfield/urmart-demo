from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Product, Order

@receiver(post_delete, sender=Order)
def back_to_stock(sender,instance, **kwargs):
    try:
        product = Product.objects.get(id=instance.product_id)
    except Product.DoesNotExits:
        return

    product.purchase(instance.qty)


@receiver(post_save, sender=Order)
def purge_from_stock(sender,instance, **kwargs):
    try:
        product = Product.objects.get(id=instance.product_id)
    except Product.DoesNotExits:
        return

    product.sold(instance.qty)

    
    
