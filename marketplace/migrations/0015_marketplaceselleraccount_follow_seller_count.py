# Generated by Django 3.2.20 on 2024-06-10 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0014_auto_20240318_1247'),
    ]

    operations = [
        migrations.AddField(
            model_name='marketplaceselleraccount',
            name='follow_seller_count',
            field=models.PositiveIntegerField(default=0, editable=False),
        ),
    ]
