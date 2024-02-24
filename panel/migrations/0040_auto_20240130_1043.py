# Generated by Django 3.1.12 on 2024-01-30 10:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0039_auto_20240129_2358'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='documentsrepository',
            name='files',
        ),
        migrations.RemoveField(
            model_name='documentsrepository',
            name='links',
        ),
        migrations.AddField(
            model_name='files',
            name='company_settings',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='panel.documentsrepository'),
        ),
        migrations.AddField(
            model_name='links',
            name='company_settings',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='panel.documentsrepository'),
        ),
        migrations.AlterField(
            model_name='files',
            name='file',
            field=models.FileField(upload_to='import', verbose_name='Dosyalar'),
        ),
    ]
