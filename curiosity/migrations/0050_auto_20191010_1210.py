# Generated by Django 2.2.4 on 2019-10-10 09:10

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('curiosity', '0049_auto_20191010_0952'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-created_date'], 'permissions': (('can_add_auto', 'Auto add auto'),)},
        ),
        migrations.AlterField(
            model_name='image',
            name='id',
            field=models.UUIDField(default=uuid.UUID('e6190f73-7dc5-48bc-a3c3-e74b97fea251'), primary_key=True, serialize=False, verbose_name='Интификатор'),
        ),
    ]