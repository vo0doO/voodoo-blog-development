import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cover_image = models.ImageField(verbose_name=None, name=None, width_field=None, height_field=None)
    title = models.CharField(max_length=200)
    text = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


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
    author = models.CharField(max_length=2000)
    step_1 = models.CharField(max_length=2000)
    step_2 = models.CharField(max_length=2000)
    step_3 = models.CharField(max_length=2000)
    step_4 = models.CharField(max_length=10)
    step_5 = models.CharField(max_length=250)
    step_6 = models.IntegerField()
    created_time = models.DateTimeField(default=timezone.now)

    def write(self):
        self.save()

    def __str__(self):
        return f"Author: {self.author}; Кому вы должны: {self.step_1}; " \
               f"Сколько: {self.step_2}; Просрочки: {self.step_3}; " \
               f"Залог: {self.step_4}; Имя: {self.step_5}; Телефон: {self.step_6}; ID: {self.id}"