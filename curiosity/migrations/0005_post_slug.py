# Generated by Django 2.2.4 on 2019-09-23 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('curiosity', '0004_auto_20190923_2000'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='slug',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]