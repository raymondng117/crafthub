from django import forms
from .models import UserAddress
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class UserAddressForm(forms.ModelForm):
    class Meta:
        model = UserAddress
        fields = ['address_line1', 'address_line2', 'city', 'state', 'country', 'postal_code']
