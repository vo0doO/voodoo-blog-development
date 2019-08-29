import uuid
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _
from multiselectfield import MultiSelectField


class Client(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ip = models.CharField(max_length=500)
    request_time = models.DateTimeField(default=timezone.now)

    def write(self):
        self.save()

    def __str__(self):
        return self.ip, self.request_time


class Question(models.Model):
    question_text = models.CharField('description', null=True, max_length=300)

    def __str__(self):
        return f"{self.question_text}"


class Choice(models.Model):
    question = models.ForeignKey(Question, null=True, on_delete=models.CASCADE)
    choice_text = models.CharField(null=True, max_length=300)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.choice_text}"


KOMU_CHOICES = (
    ('Банкам', _('Банкам')),
    ('Часным лица', _('Часным лица')),
    ('Судебным приставам', _('Судебным приставам')),
    ('МФО', _('МФО')),
    ('Другое', _('Другое')),
)

SKOLKO_CHOICES = (
    (1, _('До 200 000 руб')),
    (2, _('От 200 000 руб до 500 000 руб')),
    (3, _('От 500 000 руб до 1 000 000 руб')),
    (4, _('Более 1 000 000 руб')),
    (5, _('Более 5 000 000 руб')),
)


class Answer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.CharField(max_length=2000)
    skolko = MultiSelectField('Сколько всего вы должны ?',
        choices=SKOLKO_CHOICES,
        max_choices=1,
        max_length=500,
    )
    komu = MultiSelectField("Кому вы должны ?",
        choices=KOMU_CHOICES,
        blank=True
    )
    created_time = models.DateTimeField(default=timezone.now)

    def write(self):
        self.save()

    def __str__(self):
        return f"Автор: {self.author}, Сколько: {self.skolko}, Кому: {self.komu}"

    def __unicode__(self):
        return self.__str__()
