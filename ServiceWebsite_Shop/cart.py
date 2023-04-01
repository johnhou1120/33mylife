from ServiceWebsite_Shop.models import Product, Product_Bouns
from django.forms.models import model_to_dict
from django.conf import settings


class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CASH_CART_SESSION_ID)

        if not cart:
            cart = self.session[settings.CASH_CART_SESSION_ID] = {}

        self.cart = cart

    def __iter__(self):
        for p in self.cart.keys():
            self.cart[str(p)]['product'] = Product.objects.get(pk=p)

        for item in self.cart.values():
            item['total_price'] = item['product'].price * item['quantity']

            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def add(self, product_id, quantity=1, update_quantity=False):
        product_id = str(product_id)

        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 1, 'id': product_id}

        if update_quantity:
            self.cart[product_id]['quantity'] += int(quantity)
            
            if self.cart[product_id]['quantity'] == 0:
                self.remove(product_id)
        
        self.save()

    def remove(self, product_id):
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def save(self):
        self.session[settings.CASH_CART_SESSION_ID] = self.cart
        self.session.modified = True

    def clear(self):
        del self.session[settings.CASH_CART_SESSION_ID]
        self.session.modified = True

    def get_total_cost(self):
        for p in self.cart.keys():
            self.cart[str(p)]['product'] = Product.objects.get(pk=p)

        return sum(item['quantity'] * item['product'].price for item in self.cart.values())


class Cart_Bouns(object):
    def __init__(self, request):
        self.session = request.session
        cart_ = self.session.get(settings.BOUNS_CART_SESSION_ID)

        if not cart_:
            cart_ = self.session[settings.BOUNS_CART_SESSION_ID] = {}

        self.cart = cart_

    def __iter__(self):
        for p in self.cart.keys():
            self.cart[str(p)]['product'] = Product_Bouns.objects.get(pk=p)

        for item in self.cart.values():
            item['total_price'] = item['product'].bouns_request * item['quantity']

            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def add(self, product_id, quantity=1, update_quantity=False):
        product_id = str(product_id)

        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 1, 'id': product_id}

        if update_quantity:
            self.cart[product_id]['quantity'] += int(quantity)
            
            if self.cart[product_id]['quantity'] == 0:
                self.remove(product_id)
        
        self.save()

    def remove(self, product_id):
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def save(self):
        self.session[settings.BOUNS_CART_SESSION_ID] = self.cart
        self.session.modified = True

    def clear(self):
        del self.session[settings.BOUNS_CART_SESSION_ID]
        self.session.modified = True

    def get_total_cost(self):
        for p in self.cart.keys():
            self.cart[str(p)]['product'] = Product_Bouns.objects.get(pk=p)

        return sum(item['quantity'] * item['product'].bouns_request for item in self.cart.values())