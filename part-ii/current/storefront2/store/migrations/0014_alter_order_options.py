# Generated by Django 5.0.8 on 2024-08-19 02:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_alter_customer_options_remove_customer_email_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'permissions': [('cancel_order', 'Can cancel Order')]},
        ),
    ]
