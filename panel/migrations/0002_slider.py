# Generated by Django 3.0.7 on 2020-06-14 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Slider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('introduction', models.CharField(max_length=200)),
                ('pic', models.ImageField(blank=True, null=True, upload_to='')),
            ],
        ),
    ]
