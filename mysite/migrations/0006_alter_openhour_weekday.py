# Generated by Django 4.1 on 2022-09-14 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0005_alter_openhour_weekday'),
    ]

    operations = [
        migrations.AlterField(
            model_name='openhour',
            name='weekday',
            field=models.CharField(choices=[('Sun', 'Sunday'), ('Mon', 'Monday'), ('Tue', 'Tuesday'), ('Wed', 'Wednesday'), ('Thu', 'Thursday'), ('Fri', 'Friday'), ('Sat', 'Saturday')], max_length=100),
        ),
    ]
