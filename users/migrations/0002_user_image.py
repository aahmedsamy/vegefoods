# Generated by Django 2.2.12 on 2020-04-24 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='profiles/images', verbose_name='Profile image'),
        ),
    ]