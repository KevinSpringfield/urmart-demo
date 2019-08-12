from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db import transaction, IntegrityError
from django.db.models import Sum, F, Count
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from backstage.models import Product, Order
from .forms import NewOrderForm
from .serializers import OrderSerializer, NewOrderSerializer, ProductSerializer

from functools import wraps
import copy

ERROR = 'error'
OK = 'ok'
OUT = {
    'ret': OK,
    'msg': '',
    'data': {}
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

        if request.POST.get('vip', 'off').lower() != 'on' and product.vip:
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
    top3 = Order.objects.values('product_id').annotate(sum=Sum('qty')).order_by('-sum')[:3]

    return render(request, 'index.html', {'product_list': product_list,
                                          'order_list': order_list,
                                          'top3': top3,})


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

                updated_product = Product.objects.get(
                    id=serializer.validated_data['product_id']
                )

                out['data']['order'] = OrderSerializer(order).data
                out['data']['product'] = ProductSerializer(updated_product).data
        except IntegrityError as err:
            print(err)
            out['ret'] = ERROR
            out['msg'] = '訂單建立時發生一些錯誤，請再試一次(db integrity error)'
        except Exception as err:
            print(err)
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
        product_id = order.product_id
        order.delete()
        updated_product = Product.objects.get(id=product_id)
        
        out['data']['product'] = ProductSerializer(updated_product).data
    except Order.DoesNotExist:
        out['ret'] = ERROR
        out['msg'] = '訂單不存在'
        
        return Response(out, status=status.HTTP_404_NOT_FOUND)

    return Response(out)


@api_view(['GET'])
def report_view(request):
    shop_data = Order.objects.values('shop_id').annotate(total_qty=Sum('qty'))\
                                               .annotate(order_number=Count('id'))\
                                               .annotate(total_price=Sum(F('qty') * F('price')))

    out = ''
    for shop in shop_data:
        out += 'shop: %s, total_price: %s, total_qty: %s, order_number: %s\r\n'\
            % (shop['shop_id'], shop['total_price'], shop['total_qty'], shop['order_number'])

    response = HttpResponse(out, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=data.txt'

    return response

