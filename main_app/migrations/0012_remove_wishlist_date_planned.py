# Generated by Django 4.2.4 on 2023-08-17 04:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0011_wishlist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wishlist',
            name='date_planned',
        ),
    ]
