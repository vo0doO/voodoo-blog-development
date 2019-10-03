# Generated by Django 2.2.4 on 2019-10-03 22:23

from django.db import migrations, models
import django.utils.timezone
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0036_auto_20190930_1739'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='author',
            field=models.CharField(max_length=2000),
        ),
        migrations.AlterField(
            model_name='answer',
            name='created_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='answer',
            name='prosrochky',
            field=multiselectfield.db.fields.MultiSelectField(choices=[(1, 'Нет'), (2, 'Да, до месяца'), (1, 'Да, от месяца до трёх'), (1, 'Более трёх месяцев')], error_messages={'required': 'Обязательное поле.'}, help_text='Или любым другим платежам срок по которым уже наступил.', max_length=7, verbose_name='Есть ли у Вас просрочки по кредитам ?'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='skolko',
            field=multiselectfield.db.fields.MultiSelectField(choices=[(1, 'До 200 000 руб'), (2, 'От 200 000 руб до 500 000 руб'), (3, 'От 500 000 руб до 1 000 000 руб'), (4, 'Более 1 000 000 руб'), (5, 'Более 5 000 000 руб')], error_messages={'required': 'Обязательное поле.'}, help_text='Укажите пожалуйста приблизительный диапазон', max_length=9, verbose_name='Сколько всего Вы должны ?'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='zalogi',
            field=multiselectfield.db.fields.MultiSelectField(choices=[(1, 'Есть'), (2, 'Нет')], error_messages={'required': 'Обязательное поле.'}, help_text='Например, ипотечная квартира или             автомобиль купленный в автокредит.', max_length=3, verbose_name='Есть ли у Вас имущество в залоге ?'),
        ),
    ]
