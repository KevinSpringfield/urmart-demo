from django.contrib import admin
from backstage.models import Product, Order


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fields = ['product_id', 'stock_pcs', 'price', 'shop_id', 'vip']
    list_display = [field.name for field in Product._meta.fields]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    fields = ['product_id', 'qty', 'price', 'shop_id']
    list_display = [field.name for field in Order._meta.fields]

