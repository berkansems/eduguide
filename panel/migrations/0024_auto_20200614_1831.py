# Generated by Django 3.0.7 on 2020-06-14 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0023_auto_20200614_1735'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courses',
            name='endDate',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='courses',
            name='startDate',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
