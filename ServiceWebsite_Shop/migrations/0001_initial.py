# Generated by Django 4.0.6 on 2023-03-02 01:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ServiceWebsite_Vendor', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('slug', models.SlugField(max_length=200)),
                ('ordering', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': '產品分類',
                'verbose_name_plural': '產品分類',
                'ordering': ['ordering'],
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='訂單時間1')),
                ('paid_amount', models.DecimalField(decimal_places=0, max_digits=8)),
                ('paid', models.BooleanField(default=False)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Order', to=settings.AUTH_USER_MODEL)),
                ('vendors', models.ManyToManyField(related_name='Order', to='ServiceWebsite_Vendor.vendor')),
            ],
            options={
                'verbose_name': '商品訂單',
                'verbose_name_plural': '商品訂單',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Order_Bouns',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='訂單時間2')),
                ('bouns_spend', models.DecimalField(decimal_places=0, max_digits=8)),
                ('paid', models.BooleanField(default=False)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Order_Bouns', to=settings.AUTH_USER_MODEL)),
                ('vendors', models.ManyToManyField(related_name='Order_Bouns', to='ServiceWebsite_Vendor.vendor')),
            ],
            options={
                'verbose_name': '點數商品訂單',
                'verbose_name_plural': '點數商品訂單',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Product_Bouns',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('slug', models.SlugField(max_length=200)),
                ('description', models.TextField(blank=True, null=True)),
                ('bouns_request', models.DecimalField(decimal_places=2, max_digits=10)),
                ('added_date', models.DateTimeField(auto_now_add=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='uploads/')),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to='')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Product_Bouns', to='ServiceWebsite_Shop.category')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Product_Bouns', to='ServiceWebsite_Vendor.vendor')),
            ],
            options={
                'verbose_name': '點數商品',
                'verbose_name_plural': '點數商品',
                'ordering': ['vendor', '-added_date'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('slug', models.SlugField(max_length=200)),
                ('description', models.TextField(blank=True, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('added_date', models.DateTimeField(auto_now_add=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='uploads/')),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to='')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Product', to='ServiceWebsite_Shop.category')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Product', to='ServiceWebsite_Vendor.vendor')),
            ],
            options={
                'verbose_name': '商品',
                'verbose_name_plural': '商品',
                'ordering': ['vendor', '-added_date'],
            },
        ),
        migrations.CreateModel(
            name='OrderItem_Bouns',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='訂單時間2')),
                ('vendor_paid', models.BooleanField(default=False)),
                ('quantity', models.IntegerField(default=1)),
                ('bouns_spend', models.DecimalField(decimal_places=1, default=0, max_digits=8, verbose_name='扣除紅利點數')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='OrderItem_Bouns', to='ServiceWebsite_Shop.order_bouns')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='OrderItem_Bouns', to='ServiceWebsite_Shop.product_bouns')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='OrderItem_Bouns', to='ServiceWebsite_Vendor.vendor')),
            ],
            options={
                'verbose_name': '點數商品訂單明細',
                'verbose_name_plural': '點數商品訂單明細',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='訂單時間1')),
                ('vendor_paid', models.BooleanField(default=False)),
                ('quantity', models.IntegerField(default=1)),
                ('bouns_points', models.DecimalField(decimal_places=1, default=0, max_digits=8, verbose_name='紅利點數')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='OrderItem', to='ServiceWebsite_Shop.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='OrderItem', to='ServiceWebsite_Shop.product')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='OrderItem', to='ServiceWebsite_Vendor.vendor')),
            ],
            options={
                'verbose_name': '商品訂單明細',
                'verbose_name_plural': '商品訂單明細',
            },
        ),
    ]