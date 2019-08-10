from django import forms

class NewOrderForm(forms.Form):
    product_id = forms.IntegerField()
    qty = forms.IntegerField()
    price = forms.IntegerField()
    shop_id = forms.IntegerField()
    customer_id = forms.IntegerField()
