from django.contrib import admin
from . models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User
# Register your models here.
admin.site.register(ShippingAddress)
admin.site.register(OrderItem)
admin.site.register(Order)

class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0
    
    
class OrderAdmin(admin.ModelAdmin):
    model = Order
    readonly_fields = ['date_ordered']
    inlines = [OrderItemInline]

# Unregister order model to view newly added model to admin panel
admin.site.unregister(Order)
# re-register order and orderadmin
admin.site.register(Order, OrderAdmin)

