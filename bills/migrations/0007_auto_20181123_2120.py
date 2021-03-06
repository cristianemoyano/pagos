# Generated by Django 2.1.3 on 2018-11-24 00:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bills', '0006_bill_start_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='billstatus',
            name='code',
            field=models.CharField(default='PENDING', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='debt',
            name='detail',
            field=models.TextField(blank=True, null=True),
        ),
    ]
