from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView

from allauth.socialaccount.models import SocialAccount
from .models import Vendor
from ServiceWebsite_Shop.models import Product, Order, OrderItem, Product_Bouns, Order_Bouns, OrderItem_Bouns
from .forms import ProductForm

# Converting Title into Slug
from django.utils.text import slugify

# Create your views here.

def vendors(request):
    vendors = Vendor.objects.all()
    return render(request, 'vendor/vendors.html', {'vendors': vendors})

def vendor(request, vendor_id):
    vendor = get_object_or_404(Vendor, pk=vendor_id)
    return render(request, 'vendor/vendor.html', {'vendor': vendor})

def get_vendor(request):
    if hasattr(request.user, 'vendor_boss'):
        print(123)
        vendor = request.user.vendor_boss
    else:
        vendor = request.user.vendor_emp.first()
    return vendor

@login_required
def vendor_admin(request):
    vendor = get_vendor(request)
    return render(request, 'vendor/vendor_admin.html', {'vendor': vendor})

class vendor_products_listview(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'vendor/vendor_admin.html'
    context_object_name = 'products'
    paginate_by = 20
    
    def get_context_data(self, **kwargs):
        context = super(vendor_products_listview, self).get_context_data(**kwargs)
        context['vendor'] = get_vendor(self.request)
        pagination_data = self.get_pagination_data(context.get('paginator'), context.get('page_obj'))
        context.update(pagination_data)

        return context

    def get_queryset(self):
        vendor = get_vendor(self.request)
        return vendor.Product.all().order_by('-added_date')
    
    def get_pagination_data(self, paginator, page_obj, around_count=1):
        current_page = page_obj.number
        num_pages = paginator.num_pages

        left_has_more = False
        right_has_more = False

        if current_page<= around_count+2:
            left_pages = range(1,current_page)
        else:
            left_has_more = True
            left_pages = range(current_page-around_count, current_page)
        if current_page >= num_pages - around_count -1:
            right_pages = range(current_page+1, num_pages+1)
        else:
            right_has_more = True
            right_pages = range(current_page+1, current_page+around_count+1)
        return {
            'left_pages': left_pages, 
            'right_pages': right_pages,
            'left_has_more': left_has_more, 
            'right_has_more': right_has_more
        }

class vendor_orders_listview(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'vendor/vendor_admin.html'
    context_object_name = 'orders'
    paginate_by = 10
    
    def get_context_data(self, **kwargs):
        context = super(vendor_orders_listview, self).get_context_data(**kwargs)
        context['vendor'] = get_vendor(self.request)
        pagination_data = self.get_pagination_data(context.get('paginator'), context.get('page_obj'))
        context.update(pagination_data)

        return context

    def get_queryset(self):
        vendor = get_vendor(self.request)
        orders = vendor.Order.all()
        for order in orders:
            order.vendor_amount = 0
            order.vendor_paid_amount = 0
            order.fully_paid = True
            order.customer_social_accounts = SocialAccount.objects.filter(user=order.customer).first()

            for item in order.OrderItem.all():
                if item.vendor == vendor:
                    if item.vendor_paid:
                        order.vendor_paid_amount += item.get_total_price()
                    else:
                        order.vendor_amount += item.get_total_price()
                        order.fully_paid = False

        return orders
    
    def post(self, request):
        # print(request.POST)
        if 'item_id_paid' in request.POST:
            item_id_paid = request.POST['item_id_paid']
            item = OrderItem.objects.filter(id = item_id_paid).update(vendor_paid=True)
            return redirect('ServiceWebsite_Vendor:vendor_order_list')
        elif 'item_id_finished' in request.POST:
            item_id_finished = request.POST['item_id_finished']
            item = OrderItem.objects.filter(id = item_id_finished).update(vendor_finished=True)
            return redirect('ServiceWebsite_Vendor:vendor_order_list')
            
    
    
    def get_pagination_data(self, paginator, page_obj, around_count=1):
        current_page = page_obj.number
        num_pages = paginator.num_pages

        left_has_more = False
        right_has_more = False

        if current_page<= around_count+2:
            left_pages = range(1,current_page)
        else:
            left_has_more = True
            left_pages = range(current_page-around_count, current_page)
        if current_page >= num_pages - around_count -1:
            right_pages = range(current_page+1, num_pages+1)
        else:
            right_has_more = True
            right_pages = range(current_page+1, current_page+around_count+1)
        return {
            'left_pages': left_pages, 
            'right_pages': right_pages,
            'left_has_more': left_has_more, 
            'right_has_more': right_has_more
        }

class vendor_bounsorders_listview(LoginRequiredMixin, ListView):
    model = Order_Bouns
    template_name = 'vendor/vendor_admin.html'
    context_object_name = 'bounsorders'
    paginate_by = 10
    
    def get_context_data(self, **kwargs):
        context = super(vendor_bounsorders_listview, self).get_context_data(**kwargs)
        context['vendor'] = get_vendor(self.request)
        pagination_data = self.get_pagination_data(context.get('paginator'), context.get('page_obj'))
        context.update(pagination_data)

        return context

    def get_queryset(self):
        vendor = get_vendor(self.request)
        orders = vendor.Order_Bouns.all()
        for order in orders:
            order.vendor_amount = 0
            order.vendor_paid_amount = 0
            order.fully_paid = True
            order.customer_social_accounts = SocialAccount.objects.filter(user=order.customer).first()

            for item in order.OrderItem_Bouns.all():
                if item.vendor == vendor:
                    if item.vendor_paid:
                        order.vendor_paid_amount += item.get_total_bouns_cost()
                    else:
                        order.vendor_amount += item.get_total_bouns_cost()
                        order.fully_paid = False

        return orders
    
    def post(self, request):
        if 'item_id' in request.POST:
            item_id = request.POST['item_id']
            item = OrderItem_Bouns.objects.filter(id = item_id).update(vendor_paid=True)
        return redirect('ServiceWebsite_Vendor:vendor_bounsorder_list')

    def get_pagination_data(self, paginator, page_obj, around_count=1):
        current_page = page_obj.number
        num_pages = paginator.num_pages

        left_has_more = False
        right_has_more = False

        if current_page<= around_count+2:
            left_pages = range(1,current_page)
        else:
            left_has_more = True
            left_pages = range(current_page-around_count, current_page)
        if current_page >= num_pages - around_count -1:
            right_pages = range(current_page+1, num_pages+1)
        else:
            right_has_more = True
            right_pages = range(current_page+1, current_page+around_count+1)
        return {
            'left_pages': left_pages, 
            'right_pages': right_pages,
            'left_has_more': left_has_more, 
            'right_has_more': right_has_more
        }

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            product = form.save(commit=False) # Because we have not given vendor yet
            product.vendor = get_vendor(request)
            product.slug = slugify(product.title)
            product.save() #finally save

            return redirect('ServiceWebsite_Vendor:vendor_product_list')

    else:
        form = ProductForm

    return render(request, 'vendor/add_product.html', {'form': form})


# @login_required
# def edit_vendor(request):
#     vendor = get_vendor(request)

#     if request.method == 'POST':
#         name  = request.POST.get('name', '')
#         email = request.POST.get('email', '')

#         if name:
#             vendor.created_by.email = email
#             vendor.created_by.save()

#             vendor.name = name
#             vendor.save

#             return redirect('ServiceWebsite_Vendor:vendor-admin')

#     return render(request, 'vendor/edit_vendor.html', {'vendor': vendor})

def become_vendor(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            vendor = Vendor.objects.create(name=user.username, created_by=user)

            return redirect('ServiceWebsite:home')
    else:
        form = UserCreationForm()   

    return render(request, 'vendor/become_vendor.html', {'form': form})

