# Generated by Django 3.0.7 on 2020-06-15 07:06

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0026_student'),
    ]

    operations = [
        migrations.AddField(
            model_name='courses',
            name='createdAt',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
