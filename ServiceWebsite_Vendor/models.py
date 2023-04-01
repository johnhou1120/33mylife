from django.contrib.auth.models import User
from django.db import models
from django.db.models.fields.related import OneToOneField

# Create your models here.

VENDOR_LEVELS = (
    ('A','A級店家'),
    ('B', 'B級店家'),
    )

class Vendor(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.OneToOneField(User, related_name='vendor_boss', on_delete=models.CASCADE)
    level = models.CharField(max_length=6, choices=VENDOR_LEVELS, default='A')
    member = models.ManyToManyField(User, related_name='vendor_emp')
    
    class Meta:
        verbose_name = "供應商"
        verbose_name_plural = "供應商"
        ordering = ['name']
    
    def __str__(self):
        return self.name

    def get_balance(self):
        items = self.OrderItem.filter(vendor_paid=False, order__vendors__in=[self.id])
        return sum((item.product.price * item.quantity) for item in items)

    def get_paid_amount(self):
        items = self.OrderItem.filter(vendor_paid=True, order__vendors__in=[self.id])
        return sum((item.product.price * item.quantity) for item in items)
    
    def get_exchange_balance(self):
        items = self.OrderItem_Bouns.filter(vendor_paid=False, order__vendors__in=[self.id])
        return sum((item.product.bouns_request * item.quantity) for item in items)
    
    def get_exchange_amount(self):
        items = self.OrderItem_Bouns.filter(vendor_paid=True, order__vendors__in=[self.id])
        return sum((item.product.bouns_request * item.quantity) for item in items)