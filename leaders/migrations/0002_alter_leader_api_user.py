# Generated by Django 3.2.13 on 2022-07-11 08:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apiauth', '0008_auto_20200402_0951'),
        ('leaders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leader',
            name='api_user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='apiauth.apiuser'),
        ),
    ]
