# Generated by Django 4.2.11 on 2024-03-10 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0009_alter_customer_dry_alter_customer_gravy_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='address',
            field=models.TextField(blank=True, default=None, null=True),
        ),
    ]
