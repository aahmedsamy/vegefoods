# Generated by Django 2.2.12 on 2020-04-24 16:26

from django.db import migrations, models
import helpers.validators


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20200424_1624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(help_text="1) password length is from 8 to 128 letters.2) contains lower letters.3) contains upper letters.4) contains numbers.5) contains special characters './!@#$%&;'", max_length=128, validators=[helpers.validators.PasswordValidation], verbose_name='password'),
        ),
    ]
