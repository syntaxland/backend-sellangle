# Generated by Django 3.2.20 on 2024-02-14 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='postpaidad',
            name='ad_charge_hours',
            field=models.PositiveIntegerField(default=0, editable=False, null=True),
        ),
    ]
