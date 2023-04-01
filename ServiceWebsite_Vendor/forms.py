from django.forms import ModelForm, models

from ServiceWebsite_Shop.models import Product


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'image', 'title', 'description', 'price']