from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe


class Channel(models.Model):
    name = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField("Заголовок", max_length=250, unique=True)
    html = models.TextField("ХТМЛ")
    text = models.TextField("Русский текст")
    channel = models.ForeignKey(
        "Channel",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Рубрика"
        )
    tags = models.ManyToManyField("Tag", verbose_name="Хештеги")
    pubdate = models.DateTimeField("Дата публикации", auto_now_add=True)
    rewritedate = models.DateTimeField("Дата редактирования", auto_now=True)
    slug = models.CharField(max_length=1000, null=True)
    image = models.ImageField(null=True, blank=True, upload_to="images", verbose_name='Изображение')

    class Meta:
        ordering = ["title", "-pubdate"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post-detail", args=[str(self.id)])

    def display_tag(self):
        return ', '.join([tag.name for tag in self.tags.all()[:3]])
    display_tag.short_description = "Хештеги"

    def display_image(self):
        if self.image:
            return mark_safe('<img src="%s" width="0"></img>' % self.image.url)
        else:
            return 'none'
    display_image.short_description = 'Изображение'
    display_image.allow_tags = True