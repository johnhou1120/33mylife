from django.urls import path
from ServiceWebsite_Shop import views
from ServiceWebsite.views import cash_homepage, bouns_homepage

app_name = 'ServiceWebsite_Shop'

urlpatterns = [
    path('cash_cart/', views.cart_detail_cash, name="cash_cart"),
    path('bouns_cart/', views.cart_detail_bouns, name="bouns_cart"),
    path('', cash_homepage, name="home"),
    path('cash/', cash_homepage, name="home"),
    path('bouns/', bouns_homepage, name="bouns_home"),
    path('cash/<slug:category_slug>/', views.category_cash, name="category"),
    path('cash/<slug:category_slug>/<slug:product_slug>/', views.product_cash, name="product"),
    path('bouns/<slug:category_slug>/', views.category_bouns, name="category_bouns"),
    path('bouns/<slug:category_slug>/<slug:product_slug>/', views.product_bouns, name="product_bouns"),
    path('cash/search', views.search_cash, name="search"),
    path('bouns/search', views.search_bouns, name="search_bouns"),

    path('customs/cash/', views.success_cash, name="success"),
    path('customs/bouns/', views.success_bouns, name="success_bouns"),

    path('Add2Cart/<slug:category_slug>/<slug:product_slug>/', views.product_Add2Cart, name="Add2Cart"),
    path('Add2Cart_bouns/<slug:category_slug>/<slug:product_slug>/', views.product_Add2Cart_Bouns, name="Add2Cart_bouns"),
]