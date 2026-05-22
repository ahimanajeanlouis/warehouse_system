from django import forms
from .models import Product
from .models import Receiving

from .models import Putaway

from .models import Picking
from .models import Packing
from .models import Shipping


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'sku', 'quantity']

class ReceivingForm(forms.ModelForm):
    class Meta:
        model = Receiving
        fields = ['product_name', 'sku', 'quantity', 'supplier']

class PutawayForm(forms.ModelForm):
    class Meta:
        model = Putaway
        fields = ['product_name', 'sku', 'quantity', 'location']

class PickingForm(forms.ModelForm):
    class Meta:
        model = Picking
        fields = ['product_name', 'sku', 'quantity', 'order_reference']
        
class PackingForm(forms.ModelForm):
    class Meta:
        model = Packing
        fields = ['order_ref', 'product', 'quantity', 'status']
        
class ShippingForm(forms.ModelForm):
    class Meta:
        model = Shipping
        fields = ['order_ref', 'product', 'quantity', 'destination', 'status']