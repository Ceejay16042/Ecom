from django.contrib import admin
from my_app.models import customer, Product, Order, OrderItem, ShippingAddress

# Register your models here.
admin.site.register(Product)
admin.site.register(customer)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)



 