import stripe #pip install stripe 

from django. conf import settings
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from ServiceWebsite_Shop.cart import Cart, Cart_Bouns
from django.db.models import Q

from ServiceWebsite_Shop.forms import AddToCartForm
from ServiceWebsite_Shop.utilities import checkout, checkout_bouns, notify_vendor, notify_customer
from ServiceWebsite_Shop.models import Category, Product, Product_Bouns

import random # To get random products from the database

# Create your views here.

# cart

def cart_detail_cash(request):
    _cart = Cart(request)
    error_msg = ''
    # If Checkout
    if request.method == 'POST':
        if request.user.is_authenticated:
            order = checkout(request, _cart.get_total_cost())
            _cart.clear()
            return redirect('ServiceWebsite_Shop:success')
        else:
            messages.error(request, "未登錄使用者")
            error_msg = '未登錄使用者'

    remove_from_cart = request.GET.get('remove_from_cart', '')
    change_quantity = request.GET.get('change_quantity', '')
    quantity = request.GET.get('quantity', 0)

    if remove_from_cart:
        _cart.remove(remove_from_cart)
        return redirect('ServiceWebsite_Shop:cash_cart')
    
    if change_quantity:
        _cart.add(change_quantity, quantity, True)
        return redirect('ServiceWebsite_Shop:cash_cart')
    return render(request, 'cart/cart.html', context = {'error_msg':error_msg})

def cart_detail_bouns(request):
    _cart_bouns = Cart_Bouns(request)
    error_msg = ''
    # If Checkout
    if request.method == 'POST':
        if request.user.is_authenticated:
            total_cost = _cart_bouns.get_total_cost()

            BounsBalance, BounsTotal = get_user_bouns(request.user)
            order = checkout_bouns(request, total_cost)
            _cart_bouns.clear()
            return redirect('ServiceWebsite_Shop:success_bouns')
            # if (BounsBalance >= total_cost):
            #     order = checkout_bouns(request, total_cost)
            #     _cart_bouns.clear()
            #     return redirect('ServiceWebsite_Shop:success_bouns')
            # else:
            #     messages.error(request, "使用者點數不足")
            #     error_msg = '使用者點數不足'
            #     print(error_msg)

        else:
            messages.error(request, "未登錄使用者")
            error_msg = '未登錄使用者'
            
    remove_from_cart = request.GET.get('remove_from_cart', '')
    change_quantity = request.GET.get('change_quantity', '')
    quantity = request.GET.get('quantity', 0)

    if remove_from_cart:
        _cart_bouns.remove(remove_from_cart)
        return redirect('ServiceWebsite_Shop:bouns_cart')
    
    if change_quantity:
        _cart_bouns.add(change_quantity, quantity, True)
        return redirect('ServiceWebsite_Shop:bouns_cart')
    return render(request, 'cart/cart_bouns.html', context = {'error_msg':error_msg})

def success_cash(request):
    return render(request, 'customs/customs.html')

def success_bouns(request):
    return render(request, 'customs/customs.html')

def get_user_bouns(user):
    BounsBalance = 0
    BounsTotal = 0

    orders_cash = user.Order.all()
    for order in orders_cash:
        for item in order.OrderItem.all():
            if item.vendor_paid:
                BounsBalance += item.bouns_points
                BounsTotal += item.bouns_points
            
    orders_bouns = user.Order_Bouns.all()
    for order in orders_bouns:
        for item in order.OrderItem_Bouns.all():
            BounsBalance -= item.bouns_spend
            if item.vendor_paid:
                BounsTotal -= item.bouns_spend
    
    return BounsBalance, BounsTotal


# Products
def product_Add2Cart(request, category_slug, product_slug):
    next = request.GET.get('next', '/')
    print(next)
    cart = Cart(request)
    product = get_object_or_404(Product, category__slug=category_slug, slug=product_slug)
    # Check whether the AddToCart button is clicked or not
    cart.add(product_id=product.id, quantity=1, update_quantity=False)
    messages.success(request, "商品已加入購物車")
    return redirect(next)

def product_Add2Cart_Bouns(request, category_slug, product_slug):
    next = request.GET.get('next', '/')
    print(next)
    cart = Cart_Bouns(request)
    product = get_object_or_404(Product_Bouns, category__slug=category_slug, slug=product_slug)
    # Check whether the AddToCart button is clicked or not
    cart.add(product_id=product.id, quantity=1, update_quantity=False)
    messages.success(request, "商品已加入購物車")
    return redirect(next)

def product_cash(request, category_slug, product_slug):
    # Create instance of Cart class
    cart = Cart(request)

    product = get_object_or_404(Product, category__slug=category_slug, slug=product_slug)

    # Check whether the AddToCart button is clicked or not
    if request.method == 'POST':
        form = AddToCartForm(request.POST)

        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            cart.add(product_id=product.id, quantity=quantity, update_quantity=False)

            messages.success(request, "商品已加入購物車")

            return redirect('ServiceWebsite_Shop:product', category_slug=category_slug, product_slug=product_slug)            
    
    else:
        form = AddToCartForm()

    similar_products = list(product.category.Product.exclude(id=product.id))

    # If more than 4 similar products, then get 4 random products 
    if len(similar_products) >= 4:
        similar_products = random.sample(similar_products, 4)
    
    context = {
        'product': product,
        'similar_products': similar_products,
        'form': form,
    }

    return render(request, 'product/product.html', context)

def category_cash(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    return render(request,'product/category.html', {'category': category})

def product_bouns(request, category_slug, product_slug):
    # Create instance of Cart class
    cart_bouns = Cart_Bouns(request)

    product = get_object_or_404(Product_Bouns, category__slug=category_slug, slug=product_slug)

    # Check whether the AddToCart button is clicked or not
    if request.method == 'POST':
        form = AddToCartForm(request.POST)

        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            cart_bouns.add(product_id=product.id, quantity=quantity, update_quantity=False)

            messages.success(request, "商品已加入購物車")

            return redirect('ServiceWebsite_Shop:product_bouns', category_slug=category_slug, product_slug=product_slug)            
    
    else:
        form = AddToCartForm()

    similar_products = list(product.category.Product.exclude(id=product.id))

    # If more than 4 similar products, then get 4 random products 
    if len(similar_products) >= 4:
        similar_products = random.sample(similar_products, 4)
    
    context = {
        'product': product,
        'similar_products': similar_products,
        'form': form,
    }
    return render(request, 'product/product_bouns.html', context)

def category_bouns(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    return render(request,'product/category_bouns.html', {'category': category})

def search_cash(request):
    query = request.GET.get('query', '') # second is default parameter which is empty
    products = Product.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))

    return render(request, 'product/search.html', {'products':products, 'query': query})

def search_bouns(request):
    query = request.GET.get('query', '') # second is default parameter which is empty
    products = Product_Bouns.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))

    return render(request, 'product/search_bouns.html', {'products':products, 'query': query})