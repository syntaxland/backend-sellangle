# Generated by Django 3.2.20 on 2024-02-14 09:24

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('marketplace', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('username', models.CharField(max_length=100, unique=True)),
                ('first_name', models.CharField(blank=True, max_length=30, null=True)),
                ('last_name', models.CharField(blank=True, max_length=30, null=True)),
                ('phone_number', models.CharField(max_length=18, unique=True)),
                ('is_verified', models.BooleanField(default=False)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='images/avatars/')),
                ('referral_code', models.CharField(max_length=10, null=True, unique=True)),
                ('referral_link', models.CharField(max_length=225, null=True, unique=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_marketplace_seller', models.BooleanField(default=False)),
                ('is_ecommerce_seller', models.BooleanField(default=False)),
                ('is_terms_conditions_read', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('saved_free_ads', models.ManyToManyField(editable=False, related_name='saved_free_ads', to='marketplace.PostFreeAd')),
                ('saved_paid_ads', models.ManyToManyField(editable=False, related_name='saved_paid_ads', to='marketplace.PostPaidAd')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
                ('viewed_free_ads', models.ManyToManyField(editable=False, related_name='viewed_free_ads', to='marketplace.PostFreeAd')),
                ('viewed_paid_ads', models.ManyToManyField(editable=False, related_name='viewed_paid_ads', to='marketplace.PostPaidAd')),
            ],
            options={
                'default_related_name': 'user',
            },
        ),
    ]
