from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from allauth.socialaccount.models import SocialAccount
from ServiceWebsite_Customer.models import Register
from ServiceWebsite_Shop.models import Order
# Create your views here.

from .forms import RegisterForm

@login_required
def customs(request):
    return redirect('ServiceWebsite_Customer:customs_orderlist', 'cash')

@login_required
def customs_orders(request, order_type):
    user = request.user

    total_bouns = 0
    balanace_bouns = 0

    orders_cash = user.Order.all()
    for order in orders_cash:
        order.fully_paid = True
        for item in order.OrderItem.all():
            if item.vendor_paid:
                total_bouns += item.bouns_points
                balanace_bouns += item.bouns_points
            else:
                order.fully_paid = False
    print(balanace_bouns)
    orders_bouns = user.Order_Bouns.all()
    for order in orders_bouns:
        order.fully_paid = True
        for item in order.OrderItem_Bouns.all():
            balanace_bouns -= item.bouns_spend
            print(balanace_bouns)
            if item.vendor_paid:
                total_bouns -= item.bouns_spend
            else:
                order.fully_paid = False

    if order_type == "bouns":
        return render(request, 'customs/customs.html', {'orders_bouns': orders_bouns,'total_bouns': total_bouns, 'balance_bouns': balanace_bouns })
    else:
        return render(request, 'customs/customs.html', {'orders_cash': orders_cash,'total_bouns': total_bouns, 'balance_bouns': balanace_bouns })


def register_create_view(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        Register.objects.create(**form.cleaned_data)
        form = RegisterForm
    context = {
        'form':form
    }
    return render(request, 'vendor/register_create.html', context)