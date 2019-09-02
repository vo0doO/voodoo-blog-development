import uuid

from django.db import models
from django.db.models import ManyToManyField
from django.utils import timezone
from django.utils.translation import gettext as _
from multiselectfield import MultiSelectField
from phonenumber_field.modelfields import PhoneNumberField


KOMU_CHOICES = (
    ('Банкам', _('Банкам')),
    ('Часным лица', _('Часным лица')),
    ('Судебным приставам', _('Судебным приставам')),
    ('Микрофинансовым организациям', _('Микрофинансовым организациям')),
    ('Другое', _('Другое')),
)
SKOLKO_CHOICES = (
    (1, 'До 200 000 руб'),
    (2, 'От 200 000 руб до 500 000 руб'),
    (3, 'От 500 000 руб до 1 000 000 руб'),
    (4, 'Более 1 000 000 руб'),
    (5, 'Более 5 000 000 руб'),
)
PROSROCHKY_CHOICES = (
    (1, 'Нет'),
    (2, 'Да, до месяца'),
    (1, 'Да, от месяца до трёх'),
    (1, 'Более трёх месяцев'),
)
ZALOGI_CHOICES = (
    (1, 'Есть'),
    (2, 'Нет')
)

class Client(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ip = models.CharField(max_length=500)
    request_time = models.DateTimeField(default=timezone.now)

    def write(self):
        self.save()

    def __str__(self):
        return self.ip, self.request_time

## TODO: Переписать часть модели
## TODO: Добавить объект для каждого вопроса
## TODO: Свазать с ответом через "ForeginKey" и "Answer.pk"

class Answer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.CharField(max_length=2000)
    created_time = models.DateTimeField(default=timezone.now)

    skolko = MultiSelectField('Сколько всего Вы должны ?',
        choices=SKOLKO_CHOICES,
        max_choices=1,
        blank=False
    )

    komu = MultiSelectField("Кому Вы должны ?",
        choices=KOMU_CHOICES,
        blank=False
    )

    prosrochky = MultiSelectField('Есть ли у Вас просрочки по кредитам ?',
        choices=PROSROCHKY_CHOICES,
        max_choices=1,
        blank=False
    )

    zalogi = MultiSelectField('Есть ли у Вас имущество в залоге ? Например, ипотечная квартира или автомобиль купленный в автокредит.',
        choices=ZALOGI_CHOICES,
        max_choices=1,
        blank=False
    )

    name = models.CharField("Как Вас зовут ?", blank=False, max_length=200,  default="")

    phone = PhoneNumberField("Введите ваш телефон", blank=False, unique=False)
    
    def write(self):
        self.save()

    def __str__(self):
        return f"IP автора: {self.author}, Телефон: {self.phone}, Имя: {self.name} Сколько: {self.skolko}, Кому: {self.komu}, Залоги: {self.zalogi}"

    def __unicode__(self):
        return self.__str__()


class Question(models.Model):
    pass