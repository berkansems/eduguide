# Generated by Django 3.0.7 on 2020-06-27 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0034_auto_20200620_2232'),
    ]

    operations = [
        migrations.CreateModel(
            name='CronList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('ip', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
    ]