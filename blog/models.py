import uuid
from django.db import models
from django.urls import reverse
from django.utils import timezone as timezone
from django.utils.translation import gettext as _
from multiselectfield import MultiSelectField
from phonenumber_field.modelfields import PhoneNumberField


KOMU_CHOICES = (
    ('Банкам', _('Банкам')),
    ('Часным', _('Часным лица')),
    ('Приставам', _('Судебным приставам')),
    ('Микрофинансам', _('Микрофинансовым организациям')),
    ('Другое', _('Другое')),
)
SKOLKO_CHOICES = (
    ('До 200 000 руб', _('До 200 000 руб')),
    ('От 200 000 руб до 500 000 руб', _('От 200 000 руб до 500 000 руб')),
    ('От 500 000 руб до 1 000 000 руб', _('От 500 000 руб до 1 000 000 руб')),
    ('Более 1 000 000 руб', _('Более 1 000 000 руб')),
    ('Более 5 000 000 руб', _('Более 5 000 000 руб')),
)
PROSROCHKY_CHOICES = (
    ('Нет', _('Нет')),
    ('Да, до месяца', _('Да, до месяца')),
    ('Да, от месяца до трёх', _('Да, от месяца до трёх')),
    ('Более трёх месяцев', _('Более трёх месяцев')),
)
ZALOGI_CHOICES = (
    ('Есть', _('Есть')),
    ('Нет', _('Нет'))
)


class Client(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ip = models.CharField(max_length=500)
    request_time = models.DateTimeField(default=timezone.now)

    def write(self):
        self.save()

    def __str__(self):
        return self.ip, self.request_time


class Answer(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    author = models.CharField("Автор", max_length=2000)

    created_time = models.DateTimeField("Время создания", default=timezone.now)

    komu = MultiSelectField(
        "Кому Вы должны ?", choices=KOMU_CHOICES, max_choices=5,
        blank=False, help_text="Выберете 1 или более вариантов.", 
        error_messages={
            'invalid_list': 'Введите список значений.',
            'required': 'Обязательное поле.'
            })
    
    skolko = MultiSelectField(
        'Сколько всего Вы должны ?',
        choices=SKOLKO_CHOICES,
        max_choices=1,
        blank=False,
        help_text=f"Укажите пожалуйста приблизительный диапазон",
        error_messages={
            'required': 'Обязательное поле.'
            }
        )
    
    prosrochky = MultiSelectField(
        'Есть ли у Вас просрочки по кредитам ?',
        choices=PROSROCHKY_CHOICES,
        max_choices=1,
        blank=False,
        help_text=f"Или любым другим платежам срок по которым уже наступил.",
        error_messages={
            'required': 'Обязательное поле.'
            }
        )
    
    zalogi = MultiSelectField(
        'Есть ли у Вас имущество в залоге ?',
        choices=ZALOGI_CHOICES,
        max_choices=1,
        blank=False,
        help_text=f"Например, ипотечная квартира или \
            автомобиль купленный в автокредит.",
        error_messages={
            'required': 'Обязательное поле.'
            }
        )
    
    name = models.CharField(
        "Как Вас зовут ?",
        blank=False,
        max_length=200,
        default="",
        help_text=f"Представьтесь пожалуйста, \
             нам необходимо знать Ваше имя или псевдоним",
        error_messages={
            'required': 'Обязательное поле.'
            }
        )
    
    phone = PhoneNumberField(
        "Вот и последний шаг.",
        blank=False,
        unique=False,
        help_text=f"Введите Ваш номер телефона",
        error_messages={
            'required': 'Обязательное поле.'
            }
        )

    class Meta:
        ordering = ["-created_time"]


    def get_absolute_url(self):
        return reverse("blog:answer_detail", kwargs={"pk": self.pk})

    def __str__(self):
        return f"""
        Дата: {self.created_time}
        IP автора: {self.author},
        Телефон: {self.phone},
        Имя: {self.name},
        Сколько: {self.skolko},
        Кому: {self.komu},
        Залоги: {self.zalogi}
        """

    def __unicode__(self):
        return self.__str__()


class Question(models.Model):
    
    question_text = models.CharField("Текст вопроса", max_length=200)
    pub_date = models.DateTimeField('date_published', null=True)

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text