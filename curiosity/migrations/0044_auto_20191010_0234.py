# Generated by Django 2.2.4 on 2019-10-09 23:34

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('curiosity', '0043_auto_20191010_0143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='id',
            field=models.UUIDField(default=uuid.UUID('1ffef59e-c78e-4cdc-92af-d58887434463'), primary_key=True, serialize=False, verbose_name='Интификатор'),
        ),
    ]
