# Generated by Django 2.2.4 on 2019-10-10 02:32

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('curiosity', '0045_auto_20191010_0313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='id',
            field=models.UUIDField(default=uuid.UUID('5019177f-61ac-4bf9-a50e-fad393b09e0c'), primary_key=True, serialize=False, verbose_name='Интификатор'),
        ),
    ]