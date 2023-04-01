from django.shortcuts import render
from ServiceWebsite_Shop.models import Product, Product_Bouns

# Create your views here.

def cash_homepage(request):
    newest_products = Product.objects.all()[0:8]
    context = {
        'newest_products': newest_products,
    }
    return render(request, 'core/frontpage.html', context)

def bouns_homepage(request):
    newest_products = Product_Bouns.objects.all()[0:8]
    context = {
        'newest_products': newest_products,
    }
    return render(request, 'core/frontpage_bouns.html', context)



def contactpage(request):
    return render(request, 'core/contact.html')