# Generated by Django 3.0.7 on 2021-06-30 09:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0036_student_slugname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courses',
            name='branch',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bra', to='panel.Branch'),
        ),
        migrations.AlterField(
            model_name='courses',
            name='teacher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='teach', to='panel.Teacher'),
        ),
    ]
