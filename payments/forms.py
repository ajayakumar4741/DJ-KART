from django import forms
from . models import ShippingAddress


class ShippingForm(forms.ModelForm):
    shipping_full_name = forms.CharField(label='',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'full name'}), required=True)
    shipping_address1 = forms.CharField(label='',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'address1'}), required=True)
    shipping_address2 = forms.CharField(label='',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'address2'}), required=False)
    shipping_city = forms.CharField(label='',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'city'}), required=True)
    shipping_country = forms.CharField(label='',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'country'}), required=True)
    shipping_zipcode = forms.CharField(label='',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'zipcode'}), required=False)
    shipping_state = forms.CharField(label='',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'state'}), required=False)
    shipping_email = forms.EmailField(label='',widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'email'}), required=True)
    
    class Meta:
        model = ShippingAddress
        fields = ['shipping_full_name', 'shipping_address1', 'shipping_address2', 'shipping_city', 'shipping_country', 'shipping_zipcode', 'shipping_state', 'shipping_email']
        exclude = ['user']
        
class PaymentForm(forms.Form):
    card_name = forms.CharField(label='',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Card Name'}), required=True)
    card_number = forms.CharField(label='',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Card Number'}), required=True)
    card_exp_date = forms.CharField(label='',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Expiry Date'}), required=True)
    card_cvv_number = forms.CharField(label='',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Cvv'}), required=True)
    card_address1 = forms.CharField(label='',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Billing Address1'}), required=True)
    card_address2 = forms.CharField(label='',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Billing Address2'}), required=False)
    card_city = forms.CharField(label='',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Billing City'}), required=True)
    card_state = forms.CharField(label='',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Billing State'}), required=True)
    card_country = forms.CharField(label='',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Billing Country'}), required=True)
    card_zipcode = forms.CharField(label='',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Billing Zipcode'}), required=True)