from rest_framework import serializers
from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['product_id', 'qty', 'price', 'shop_id', 'customer_id']


class NewOrderSerializer(serializers.ModelSerializer):
    vip = serializers.BooleanField()

    class Meta:
        model = Order
        fields = ['product_id', 'qty', 'customer_id', 'vip']



    
