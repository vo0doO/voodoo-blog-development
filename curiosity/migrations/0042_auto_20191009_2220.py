# Generated by Django 2.2.4 on 2019-10-09 19:20

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('curiosity', '0041_auto_20191009_0141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='id',
            field=models.UUIDField(default=uuid.UUID('e69d8924-d22e-4dd6-b1ff-8a9dfc3c455f'), primary_key=True, serialize=False, verbose_name='Интификатор'),
        ),
    ]
