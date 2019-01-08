# Generated by Django 2.0.10 on 2019-01-08 12:15

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('experiments', '0015_auto_20181220_1426'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experiment',
            name='default_max_places',
            field=models.PositiveSmallIntegerField(default=1, help_text='experiment:attribute:default_max_places:help_text', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)], verbose_name='experiment:attribute:default_max_places'),
        ),
        migrations.AlterField(
            model_name='timeslot',
            name='max_places',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)], verbose_name='time_slot:attribute:max_places'),
        ),
    ]
