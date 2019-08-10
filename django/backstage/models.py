from django.db import models

# Create your models here.
class Product(models.Model):
    UM = 'um'
    MS = 'ms'
    PS = 'ps'
    SHOPS = [
        (UM, UM),
        (MS, MS),
        (PS, PS),
    ]

    product_id = models.IntegerField('商品ID', unique=True)
    stock_pcs = models.IntegerField('商品庫存數量', default=0)
    price = models.IntegerField('商品單價', default=0)
    shop_id = models.CharField('商品所屬館別', choices=SHOPS, max_length=2)
    vip = models.BooleanField('VIP限定商品', default=False)

    def __str__(self):
        return str(self.product_id)

    def sold(self, number):
        if self.stock_pcs - number < 0:
            raise ValueError('庫存不足')
        self.stock_pcs -= number
        self.save(update_fields=['stock_pcs'])

    def purchase(self, number):
        self.stock_pcs += number
        self.save(update_fields=['stock_pcs'])
        

class Order(models.Model):
    product_id = models.IntegerField('商品ID')
    qty = models.IntegerField('購買數量', default=0)
    price = models.IntegerField('商品單價', default=0)
    shop_id = models.CharField('商品所屬館別', max_length=2)
    customer_id = models.IntegerField('顧客ID')

    def __str__(self):
        return 'Product:{0}-Qty:{1}'.format(self.product_id, self.qty)
