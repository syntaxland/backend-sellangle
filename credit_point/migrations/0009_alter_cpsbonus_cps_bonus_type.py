# Generated by Django 3.2.20 on 2024-03-09 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('credit_point', '0008_auto_20240309_1500'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cpsbonus',
            name='cps_bonus_type',
            field=models.CharField(blank=True, choices=[('Referral Bonus', 'Referral Bonus'), ('Sign-up Bonus', 'Sign-up Bonus'), ('Birthday Bonus', 'Birthday Bonus'), ('Loyalty Bonus', 'Loyalty Bonus'), ('Earned Bonus', 'Earned Bonus'), ('Other Bonus', 'Other Bonus')], editable=False, max_length=100, null=True),
        ),
    ]