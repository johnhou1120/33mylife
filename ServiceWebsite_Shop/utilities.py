from ServiceWebsite_Shop.cart import Cart, Cart_Bouns

from django.conf import settings
# for HTML Email
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from ServiceWebsite_Shop.models import Order, OrderItem, Order_Bouns, OrderItem_Bouns


def checkout(request, amount):
    order = Order.objects.create(paid_amount=amount, customer = request.user)
    for item in Cart(request):
        OrderItem.objects.create(order=order, product=item['product'], vendor=item['product'].vendor, quantity=item['quantity'], bouns_points=item['product'].price*item['quantity']/10)
        order.vendors.add(item['product'].vendor)
        
    return order

def checkout_bouns(request, amount):
    order_bouns = Order_Bouns.objects.create(bouns_spend=amount, customer = request.user)
    for item in Cart_Bouns(request):
        OrderItem_Bouns.objects.create(order=order_bouns, bouns_spend=amount, product=item['product'], vendor=item['product'].vendor, quantity=item['quantity'])
        order_bouns.vendors.add(item['product'].vendor)
        
    return order_bouns

def notify_vendor(order):
    from_email = settings.DEFAULT_EMAIL_FROM

    for vendor in order.vendors.all():
        to_email = vendor.created_by.email
        subject = 'New order'
        text_content = 'You have a new order!'
        html_content = render_to_string('order/email_notify_vendor.html', {'order': order, 'vendor': vendor})

        msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
        msg.attach_alternative(html_content, 'text/html')
        msg.send()

def notify_customer(order):
    from_email = settings.DEFAULT_EMAIL_FROM

    to_email = order.email
    subject = 'Order confirmation'
    text_content = '感謝您的購買!'
    html_content = render_to_string('order/email_notify_customer.html', {'order': order})

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()