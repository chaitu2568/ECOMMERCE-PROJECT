# Generated by Django 2.2.1 on 2019-07-13 23:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_auto_20190627_2251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='billing_address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='billing_address', to='addresses.Address'),
        ),
        migrations.AlterField(
            model_name='order',
            name='billing_profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='billing.BillingProfile'),
        ),
        migrations.AlterField(
            model_name='order',
            name='cart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='carts.Cart'),
        ),
        migrations.AlterField(
            model_name='order',
            name='shipping_address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='shipping_address', to='addresses.Address'),
        ),
    ]
