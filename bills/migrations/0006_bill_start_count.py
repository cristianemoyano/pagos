# Generated by Django 2.1.3 on 2018-11-23 00:00

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('bills', '0005_auto_20181120_0001'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill',
            name='start_count',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
