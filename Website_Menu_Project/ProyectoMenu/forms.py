from django import forms
from .models import Product, BakeryClass

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image']

class BakeryClassForm(forms.ModelForm):
    class Meta:
        model = BakeryClass
        fields = ['name', 'description', 'class_level']