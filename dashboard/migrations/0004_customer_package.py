# Generated by Django 4.2.11 on 2024-03-09 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_remove_customer_email_remove_customer_service'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='package',
            field=models.TextField(blank=True),
        ),
    ]