# Generated by Django 4.2.3 on 2024-08-24 13:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('credit_point', '0004_alter_buycreditpoint_amount_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='sellcpstosellangle',
            name='cps_sold_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cps_sold_by_user', to=settings.AUTH_USER_MODEL),
        ),
    ]