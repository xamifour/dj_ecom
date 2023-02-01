from django import forms

from .models import Seller, ProductBatch


#Forms Here

class SellerForm(forms.ModelForm):
    class Meta:
        model      = Seller
        fields     = '__all__'
        exclude    = ['owner',]


class ProductBatchForm(forms.ModelForm):

    arrival_Date = forms.DateTimeField(
        widget=forms.TextInput(
            attrs={
                'type': 'date',
            }
        ),
        required=True)
        	
    class Meta:
        model      = ProductBatch
        fields     = '__all__'
        exclude    = ['seller',]

