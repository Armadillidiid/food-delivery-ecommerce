# Generated by Django 4.1 on 2022-09-11 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, default='anonymous-avatar.png', null=True, upload_to=''),
        ),
    ]