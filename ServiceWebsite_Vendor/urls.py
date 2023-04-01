from django.urls import path
from ServiceWebsite_Vendor import views
from django.contrib.auth import views as auth_views


app_name = 'ServiceWebsite_Vendor'


urlpatterns = [
    path('', views.vendors, name="vendors"),
    path('<int:vendor_id>/', views.vendor, name="vendor"),

    path('vendor-admin/', views.vendor_admin, name="vendor-admin"),
    path('vendor-admin/product_list/', views.vendor_products_listview.as_view(), name="vendor_product_list"), 
    path('vendor-admin/order_list/', views.vendor_orders_listview.as_view(), name="vendor_order_list"), 
    path('vendor-admin/bounsorder_list/', views.vendor_bounsorders_listview.as_view(), name="vendor_bounsorder_list"), 

    path('add-product/', views.add_product, name="add-product"),

    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path('login/', auth_views.LoginView.as_view(template_name='vendor/login.html'), name="login"),

    # path('edit-vendor/', views.edit_vendor, name="edit-vendor"),

    # path('become-vendor/', views.become_vendor, name="become-vendor"),
]
