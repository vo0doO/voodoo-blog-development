# Generated by Django 2.2.4 on 2019-10-01 09:38

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('curiosity', '0010_auto_20190930_1739'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(location='d:/media/images'), upload_to='', verbose_name='Изображение'),
        ),
    ]
