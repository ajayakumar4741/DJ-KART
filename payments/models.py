from django.db import models
from django.contrib.auth.models import User
from ecomstore.models import Product
from django.db.models.signals import post_save
# Create your models here.

class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    shipping_full_name = models.CharField(max_length=50)
    shipping_address1 = models.CharField(max_length=200, blank=True)
    shipping_address2 = models.CharField(max_length=20, blank=True, null=True)
    shipping_city = models.CharField(max_length=20, blank=True)
    shipping_country = models.CharField(max_length=20, blank=True)
    shipping_zipcode = models.CharField(max_length=20, blank=True, null=True)
    shipping_state = models.CharField(max_length=20, blank=True, null=True)
    shipping_email = models.EmailField()
    
    class Meta:
        verbose_name_plural = 'Shipping Address'
        
    def __str__(self):
        return f'Shipping Address - {str(self.id)}'
    
def create_shipping(sender, instance, created, **kwargs):
        if created:
            user_shipping = ShippingAddress(user=instance)
            user_shipping.save()
post_save.connect(create_shipping, sender=User)
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=20)
    email = models.EmailField()
    shipping_address = models.TextField()
    amount_paid = models.DecimalField(max_digits=20, decimal_places=2)
    date_ordered = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Order - {str(self.id)}'
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveBigIntegerField(default=1)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    
    def __str__(self):
        return f'Order Item - {str(self.id)}'