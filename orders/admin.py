from django.contrib import admin
from .models import Order, OrderProducts


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "profile",
        "totalCost",
        "status",
        "paymentType",
        "deliveryType",
        "city",
        "createdAt",
    ]
    list_filter = [
        "profile",
        "status",
        "paymentType",
        "deliveryType",
        "city",
        "createdAt",
    ]
    search_fields = ["profile"]


@admin.register(OrderProducts)
class OrderProductsAdmin(admin.ModelAdmin):
    list_display = ["order", "product", "count"]
    list_filter = ["count", "product"]
    search_fields = ["order"]
