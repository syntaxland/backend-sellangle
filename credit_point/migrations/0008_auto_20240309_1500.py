# Generated by Django 3.2.20 on 2024-03-09 14:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('credit_point', '0007_alter_adchargecreditpoint_ad_charge_cps_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buycreditpoint',
            name='cps_purchase_id',
            field=models.CharField(max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='buyusdcreditpoint',
            name='usd_cps_purchase_id',
            field=models.CharField(blank=True, max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='sellcreditpoint',
            name='cps_sell_id',
            field=models.CharField(blank=True, max_length=20, unique=True),
        ),
        migrations.CreateModel(
            name='CpsBonus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cps_bonus_type', models.CharField(blank=True, choices=[('1', '1,000 cps for USD 1'), ('5', '5,200 cps for USD 5'), ('10', '10,800 cps for USD 10'), ('15', '16,500 cps for USD 15'), ('20', '24,000 cps for USD 20'), ('60', '60,000 cps for USD 50'), ('100', '125,000 cps for USD 100'), ('200', '255,000 cps for USD 200'), ('500', '700,000 cps for USD 500'), ('1000', '1,500,000 cps for USD 1,000')], editable=False, max_length=100, null=True)),
                ('cps_amount', models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=10)),
                ('cps_bonus_id', models.CharField(blank=True, max_length=20, unique=True)),
                ('old_bal', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('new_bal', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('is_success', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cps_bonus_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]