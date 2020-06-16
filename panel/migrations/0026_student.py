# Generated by Django 3.0.7 on 2020-06-15 03:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0025_auto_20200614_2046'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('telephone', models.CharField(max_length=15)),
                ('appDate', models.DateTimeField(auto_now_add=True)),
                ('appStatus', models.CharField(choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')], default='Pending', max_length=50, null=True)),
                ('courseName', models.ManyToManyField(to='panel.Courses')),
            ],
        ),
    ]