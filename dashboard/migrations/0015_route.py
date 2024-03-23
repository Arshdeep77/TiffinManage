# Generated by Django 4.2.11 on 2024-03-10 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0014_customer_route'),
    ]

    operations = [
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rno', models.DecimalField(decimal_places=0, default=0, max_digits=10, null=True)),
            ],
        ),
    ]