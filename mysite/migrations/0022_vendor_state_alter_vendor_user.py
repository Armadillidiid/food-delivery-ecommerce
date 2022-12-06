# Generated by Django 4.1 on 2022-11-18 18:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0021_remove_vendor_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='state',
            field=models.CharField(choices=[('abia', 'Abia'), ('adamawa', 'Adamawa'), ('akwaibom', 'Akwaibom'), ('anambra', 'Anambra'), ('bauchi', 'Bauchi'), ('bayelsa', 'Bayelsa'), ('benue', 'Benue'), ('borno', 'Borno'), ('crossriver', 'Crossriver'), ('delta', 'Delta'), ('ebonyi', 'Ebonyi'), ('edo', 'Edo'), ('ekiti', 'Ekiti'), ('enugu', 'Enugu'), ('gombe', 'Gombe'), ('imo', 'Imo'), ('jigawa', 'Jigawa'), ('kaduna', 'Kaduna'), ('kano', 'Kano'), ('katsina', 'Katsina'), ('kebbi', 'Kebbi'), ('kogi', 'Kogi'), ('kwara', 'Kwara'), ('lagos', 'Lagos'), ('nasarawa', 'Nasarawa'), ('niger', 'Niger'), ('ogun', 'Ogun'), ('ondo', 'Ondo'), ('osun', 'Osun'), ('oyo', 'Oyo'), ('plateau', 'Plateau'), ('rivers', 'Rivers'), ('sokoto', 'Sokoto'), ('taraba', 'Taraba'), ('yobe', 'Yobe'), ('zamfara', 'Zamfara')], default='abia', max_length=100),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='user',
            field=models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]