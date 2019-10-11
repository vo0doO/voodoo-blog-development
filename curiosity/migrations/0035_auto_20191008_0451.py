# Generated by Django 2.2.4 on 2019-10-08 01:51

from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('curiosity', '0034_auto_20191008_0238'),
    ]

    operations = [
        migrations.AddField(
            model_name='log',
            name='created_at',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, verbose_name='Дата обнаружения'),
        ),
        migrations.AlterField(
            model_name='image',
            name='id',
            field=models.UUIDField(default=uuid.UUID('28117b1b-0cc0-4583-8f2b-6e52cd5cf667'), primary_key=True, serialize=False, verbose_name='Интификатор'),
        ),
        migrations.AlterField(
            model_name='log',
            name='text',
            field=models.TextField(max_length=5000, null=True, verbose_name='Текст'),
        ),
    ]
