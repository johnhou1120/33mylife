from ServiceWebsite_Shop.cart import Cart, Cart_Bouns
from ServiceWebsite_Shop.models import Category, Product_Bouns
from ServiceWebsite_Vendor.models import *
from allauth.socialaccount.models import SocialAccount
from django.db.models import Q



def cart_cash(request):
    cart_cash = Cart(request)
    return {'cart': cart_cash}

def cart_bouns(request):
    cart_bouns = Cart_Bouns(request)
    return {'cart_bouns': cart_bouns} 

def menu_categories(request):
    categories = Category.objects.all()
    
    product_bouns = Product_Bouns.objects.distinct('category').order_by('category_id')
    categories_bouns = []
    for product in product_bouns:
        categories_bouns.append(product.category)
    
    return {'categories': categories, 'categories_bouns': categories_bouns}

def social_accounts_data(request):
    if request.user.is_authenticated:
        social_accounts = SocialAccount.objects.filter(user=request.user).first()
        if social_accounts:
            return {'social_accounts_extra_data': social_accounts.extra_data}
    return {}

def is_vendor_mamber(request):
    user = request.user
    rtn_dict = {}
    if user.is_authenticated:
        if hasattr(user, 'vendor_boss'):
            rtn_dict['is_vendor_boss'] = True
            rtn_dict['Main_vendor'] = user.vendor_boss

        vendors = user.vendor_emp.all()
        if vendors:
            rtn_dict['vendors'] = vendors
    return rtn_dict