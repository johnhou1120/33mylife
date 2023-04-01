from django.contrib import admin
from ServiceWebsite_Shop.models import *

# Register your models here.

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)

admin.site.register(Product_Bouns)
admin.site.register(Order_Bouns)
admin.site.register(OrderItem_Bouns)