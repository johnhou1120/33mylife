from django.urls import path
from ServiceWebsite import views

app_name = 'ServiceWebsite'


urlpatterns = [
    path('', views.cash_homepage, name="home"),
    path('contact-us/', views.contactpage, name="contact"),
]
