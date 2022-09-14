# Generated by Django 4.1 on 2022-09-14 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0004_vendor_banner_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='openhour',
            name='weekday',
            field=models.CharField(choices=[('sun', 'Sunday'), ('mon', 'Monday'), ('tue', 'Tuesday'), ('wed', 'Wednesday'), ('thu', 'Thursday'), ('fri', 'Friday'), ('sat', 'Saturday')], max_length=100),
        ),
    ]
