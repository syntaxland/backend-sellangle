# Generated by Django 3.2.20 on 2024-01-15 08:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('send_email_message', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sendemailmessage',
            name='receiver_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='email_receiver', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='sendemailmessage',
            name='sender_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='email_sender', to=settings.AUTH_USER_MODEL),
        ),
    ]
