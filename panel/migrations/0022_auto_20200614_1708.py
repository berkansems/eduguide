# Generated by Django 3.0.7 on 2020-06-14 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0021_auto_20200614_1626'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courses',
            name='endDate',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='courses',
            name='startDate',
            field=models.DateTimeField(),
        ),
    ]
