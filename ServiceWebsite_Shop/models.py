from django.db import models
from django.contrib.auth.models import User
# Form Images
from io import BytesIO
from os import name
from PIL import Image
from django.core.files import File

from ServiceWebsite_Vendor.models import Vendor
from slugify import slugify
import django.utils.timezone as timezone

# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=200)
    ordering = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "產品分類"
        verbose_name_plural = "產品分類"
        ordering = ['ordering']

    def __str__(self):
        return self.title


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='Product', on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, related_name="Product", on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=200)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    added_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='', blank=True, null=True) # Change uploads to thumbnails 

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Product, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "商品"
        verbose_name_plural = "商品"
        ordering = ['vendor', '-added_date']

    def __str__(self):
        return self.title

    
    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()
                return self.thumbnail.url
            
            else:
                # Default Image
                return 'https://via.placeholder.com/240x180.jpg'
    
    # Generating Thumbnail - Thumbnail is created when get_thumbnail is called
    def make_thumbnail(self, image, size=(300, 200)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)

        thumbnail = File(thumb_io, name=image.name)

        return thumbnail

class Order(models.Model):
    customer = models.ForeignKey(User, related_name='Order', on_delete=models.CASCADE)
    created_at = models.DateTimeField('訂單時間1',default = timezone.now)
    paid_amount = models.DecimalField(max_digits=8, decimal_places=0)
    vendors = models.ManyToManyField(Vendor, related_name="Order")
    paid = models.BooleanField(default = False)

    class Meta:
        verbose_name = "商品訂單"
        verbose_name_plural = "商品訂單"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.id} | {self.customer} | {self.created_at} | {self.paid_amount} "

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="OrderItem", on_delete=models.CASCADE)
    created_at = models.DateTimeField('訂單時間1',default = timezone.now)
    product = models.ForeignKey(Product, related_name="OrderItem", on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, related_name="OrderItem", on_delete=models.CASCADE)
    vendor_paid = models.BooleanField(default=False)
    vendor_finished = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)
    bouns_points = models.DecimalField(max_digits=8, default = 0, decimal_places=1, verbose_name = "紅利點數")
    t_price = models.DecimalField(max_digits=8, decimal_places=0)

    class Meta:
        verbose_name = "商品訂單明細"
        verbose_name_plural = "商品訂單明細"

    def __str__(self):
        return f"{self.id} | {self.order.customer} | {self.created_at} | {self.vendor} | {self.product} "

    def get_total_price(self):
        return self.product.price * self.quantity
    
    def save(self, *args, **kwargs):
        self.t_price = self.get_total_price()
        super().save(*args, **kwargs)

class Product_Bouns(models.Model):
    category = models.ForeignKey(Category, related_name='Product_Bouns', on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, related_name="Product_Bouns", on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=200)
    description = models.TextField(blank=True, null=True)
    bouns_request = models.DecimalField(max_digits=10, decimal_places=2)
    added_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='', blank=True, null=True) # Change uploads to thumbnails 

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Product_Bouns, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "點數商品"
        verbose_name_plural = "點數商品"
        ordering = ['vendor', '-added_date']

    def __str__(self):
        return self.title

    
    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()
                return self.thumbnail.url
            
            else:
                # Default Image
                return 'https://via.placeholder.com/240x180.jpg'
    
    # Generating Thumbnail - Thumbnail is created when get_thumbnail is called
    def make_thumbnail(self, image, size=(300, 200)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)

        thumbnail = File(thumb_io, name=image.name)

        return thumbnail

class Order_Bouns(models.Model):
    customer = models.ForeignKey(User, related_name='Order_Bouns', on_delete=models.CASCADE)
    created_at = models.DateTimeField('訂單時間2',default = timezone.now)
    bouns_spend = models.DecimalField(max_digits=8, decimal_places=0)
    vendors = models.ManyToManyField(Vendor, related_name="Order_Bouns")
    paid = models.BooleanField(default = False)

    class Meta:
        verbose_name = "點數商品訂單"
        verbose_name_plural = "點數商品訂單"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.id} | {self.customer} | {self.created_at} | {self.bouns_spend} "

class OrderItem_Bouns(models.Model):
    order = models.ForeignKey(Order_Bouns, related_name="OrderItem_Bouns", on_delete=models.CASCADE)
    created_at = models.DateTimeField('訂單時間2',default = timezone.now)
    product = models.ForeignKey(Product_Bouns, related_name="OrderItem_Bouns", on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, related_name="OrderItem_Bouns", on_delete=models.CASCADE)
    vendor_paid = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)
    bouns_spend = models.DecimalField(max_digits=8, default = 0, decimal_places=1, verbose_name = "扣除紅利點數")
    t_bouns = models.DecimalField(max_digits=8, decimal_places=0)

    class Meta:
        verbose_name = "點數商品訂單明細"
        verbose_name_plural = "點數商品訂單明細"

    def __str__(self):
        return f"{self.id} | {self.order.customer} | {self.created_at} | {self.vendor} | {self.product} "

    def get_total_bouns_cost(self):
        return self.product.bouns_request * self.quantity
    
    def save(self, *args, **kwargs):
        self.t_bouns = self.get_total_bouns_cost()
        super().save(*args, **kwargs)