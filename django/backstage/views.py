from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db import transaction, IntegrityError
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from backstage.models import Product, Order
from .forms import NewOrderForm
from .serializers import OrderSerializer, NewOrderSerializer

from functools import wraps
import copy

ERROR = 'error'
OK = 'ok'
OUT = {
    'ret': OK,
    'msg': '',
    'data': ''
}


def validate_vip(view_func): # Replace the passed-in function with decorator when initialing
    def decorator(request, *args, **kwargs):
        out = copy.deepcopy(OUT)

        try:
            product = Product.objects.get(id=request.POST.get('product_id'))
        except Product.DoesNotExist:
            out['ret'] = ERROR
            out['msg'] = '此商品不存在'

            return Response(out)

        if request.POST.get('vip').lower() != 'true' and product.vip:
            # If you are not vip and buy vip's product
            out['ret'] = ERROR
            out['msg'] = '您無法購買該商品'

            return Response(out)
        else:
            return view_func(request, *args, **kwargs)
    return decorator


def check_stock(view_func):
    def decorator(request, *args, **kwargs):
        out = copy.deepcopy(OUT)
        
        # Check if product_id is correct
        try:
            product = Product.objects.get(id=request.POST.get('product_id'))
        except Product.DoesNotExist:
            out['ret'] = ERROR
            out['msg'] = '此商品不存在'

            return Response(out)

        # Check quantity of product in stock
        try: 
            print(int(request.POST.get('qty')), product.stock_pcs)
            if product.stock_pcs - int(request.POST.get('qty')) < 0:
                out['ret'] = ERROR
                out['msg'] = '庫存不足'

                return Response(out)
            else:
                return view_func(request, *args, **kwargs)
        except ValueError:
            out['ret'] = ERROR
            out['msg'] = '購買數量錯誤'

            return Response(out)
    return decorator


def home(request):
    product_list = Product.objects.all()
    order_list = Order.objects.all()

    return render(request, 'index.html', {'product_list': product_list,
                                          'order_list': order_list})


@api_view(['POST'])
@check_stock
@validate_vip
def new_order(request):
    out = copy.deepcopy(OUT)

    serializer = NewOrderSerializer(data=request.POST)
    if serializer.is_valid():
        try:
            with transaction.atomic():
                product = Product.objects.get(
                    id=serializer.validated_data['product_id']
                )

                order = Order.objects.create(product_id=serializer.validated_data['product_id'],
                                             qty=serializer.validated_data['qty'],
                                             price=product.price,
                                             shop_id=product.shop_id,
                                             customer_id=serializer.validated_data['customer_id'])

                out['data'] = OrderSerializer(order).data
        except IntegrityError as err:
            print(err)
            out['ret'] = ERROR
            out['msg'] = '訂單建立時發生一些錯誤，請再試一次(db integrity error)'
        except Exception as err:
            out['ret'] = ERROR
            out['msg'] = '訂單建立時發生一些錯誤，請再試一次'
    else:
        print(serializer.errors)
        out['ret'] = ERROR
        out['msg'] = '訂單錯誤'

    return Response(out)


@api_view(['DELETE'])
def delete_order(request, id):
    out = copy.deepcopy(OUT)

    try:
        order = Order.objects.get(id=id)
        order.delete()
    except Order.DoesNotExist:
        out['ret'] = ERROR
        out['msg'] = '訂單不存在'
        
        return Response(out, status=status.HTTP_404_NOT_FOUND)

    return Response(out)
