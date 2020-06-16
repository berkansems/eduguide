# Generated by Django 3.0.7 on 2020-06-14 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0024_auto_20200614_1831'),
    ]

    operations = [
        migrations.AddField(
            model_name='courses',
            name='status',
            field=models.BooleanField(default=True, verbose_name='Active ?1'),
        ),
        migrations.AlterField(
            model_name='courses',
            name='endDate',
            field=models.CharField(max_length=50, verbose_name='End Date (mm/dd/2020)'),
        ),
        migrations.AlterField(
            model_name='courses',
            name='pic',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='Select an image file'),
        ),
        migrations.AlterField(
            model_name='courses',
            name='startDate',
            field=models.CharField(max_length=50, verbose_name='Start Date (mm/dd/2020)'),
        ),
    ]