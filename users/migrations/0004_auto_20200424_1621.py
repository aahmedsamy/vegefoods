# Generated by Django 2.2.12 on 2020-04-24 16:21

from django.db import migrations, models
import helpers.validators


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20200424_1452'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=150, validators=[helpers.validators.PasswordValidation], verbose_name='password'),
        ),
    ]
