from django.contrib import admin # type: ignore
from .models import Category, Order, OrderItem, Product # type: ignore

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
