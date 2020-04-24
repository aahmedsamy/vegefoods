# Generated by Django 2.2.12 on 2020-04-24 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_delete_test'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='email_verification_code',
            field=models.CharField(blank=True, max_length=6, null=True, verbose_name='Email verification code'),
        ),
        migrations.AddField(
            model_name='user',
            name='email_verified',
            field=models.BooleanField(default=False, verbose_name='Email verified'),
        ),
        migrations.AddField(
            model_name='user',
            name='phone_number_verification_code',
            field=models.CharField(blank=True, max_length=6, null=True, verbose_name='Phone number verification code'),
        ),
        migrations.AddField(
            model_name='user',
            name='phone_number_verified',
            field=models.BooleanField(default=False, verbose_name='Phone number verified'),
        ),
    ]