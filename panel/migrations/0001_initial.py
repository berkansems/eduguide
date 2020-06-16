# Generated by Django 3.0.7 on 2020-06-13 18:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('telephone', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('place', models.CharField(max_length=50)),
                ('introduction', models.CharField(max_length=500)),
                ('startDate', models.DateTimeField()),
                ('endDate', models.DateTimeField()),
                ('telephone', models.IntegerField()),
                ('fee', models.DecimalField(decimal_places=2, max_digits=4)),
                ('capacity', models.IntegerField()),
                ('reservation', models.IntegerField(default=0)),
                ('pic', models.ImageField(blank=True, null=True, upload_to='')),
                ('status', models.BooleanField(default=True)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='panel.Branch')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='panel.Teacher')),
            ],
        ),
    ]