from django.contrib import admin
from . models import ShippingAddress, Order, OrderItem
# Register your models here.
admin.site.register(ShippingAddress)
admin.site.register(OrderItem)
admin.site.register(Order)
