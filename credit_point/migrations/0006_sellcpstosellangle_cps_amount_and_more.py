# Generated by Django 4.2.3 on 2024-08-24 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('credit_point', '0005_sellcpstosellangle_cps_sold_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='sellcpstosellangle',
            name='cps_amount',
            field=models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=10),
        ),
        migrations.AddField(
            model_name='sellcreditpoint',
            name='cps_amount',
            field=models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=10),
        ),
    ]
