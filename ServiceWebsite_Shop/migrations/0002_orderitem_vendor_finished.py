# Generated by Django 4.0.6 on 2023-03-04 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ServiceWebsite_Shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='vendor_finished',
            field=models.BooleanField(default=False),
        ),
    ]
