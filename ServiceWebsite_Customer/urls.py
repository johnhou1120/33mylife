from django.urls import path
from ServiceWebsite_Customer import views
from django.contrib.auth import views as auth_views


app_name = 'ServiceWebsite_Customer'


urlpatterns = [
    path('', views.customs, name="customs"),
    path('<str:order_type>/', views.customs_orders, name="customs_orderlist"),
    # path('register/', views.register_create_view, name="register_create_view"),
]
