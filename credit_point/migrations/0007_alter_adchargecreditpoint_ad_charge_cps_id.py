# Generated by Django 3.2.20 on 2024-02-15 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('credit_point', '0006_adchargecreditpoint'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adchargecreditpoint',
            name='ad_charge_cps_id',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
