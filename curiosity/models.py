import os
import uuid
import platform
from django.db import models
from django.urls import reverse
from django.utils import timezone as timezone
from django.utils.safestring import mark_safe
from django.core.files.storage import FileSystemStorage


class Channel(models.Model):
    name = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return self.name.capitalize()


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Image(models.Model):
    id = models.UUIDField("Интификатор", primary_key=True, default=uuid.uuid4(), editable=True)
    created_time = models.DateTimeField("Время создания", default=timezone.now)

    # post = models.ForeignKey(
    #     'Post',
    #     on_delete=models.SET_NULL,
    #     verbose_name="Пост",
    #     null=True
    #     )
    url_prefix = models.CharField("Префикс", max_length=len("https://dw8stlw9qt0iz.cloudfront.net/"), default="https://dw8stlw9qt0iz.cloudfront.net/")
    urls_x300 = models.TextField(verbose_name="Размеры x300", default=None, null=True)
    urls_x600 = models.TextField(verbose_name="Размеры x600", default=None, null=True)
    url_sufix = models.CharField("Суфикс", max_length=len(".png"), default=".png")

    ROLE = (
        ('о', 'Обложка'),
        ('б1', "Блок 1"),
        ('б2', "Блок 2"),
        ('б3', "Блок 3"),
    )

    role = models.CharField(
        "Позиция",
        max_length=2,
        choices=ROLE,
        blank=True,
        default='о',
    )

    class Meta:
        ordering = ['created_time']
        
        
    def nice_x300_url(self, size):
        path_list = self.urls_x300.split(', ')
        return self.url_prefix + path_list[size] + self.url_sufix
    
    
    def nice_x600_url(self, size):
        path_list = self.urls_x600.split(', ')
        return self.url_prefix + path_list[size] + self.url_sufix
    
    
    def get_storage(unix_pref, windows_pref):
        plat = platform.system()
        if plat == "Windows":
            return FileSystemStorage(location=os.path.join(windows_pref, "media"))
        elif plat != "Linux":
            return FileSystemStorage(location=os.path.join(unix_pref, "media"))
        else:
            return FileSystemStorage(location="")


    def get_path(self):
        pass
        #     if self.img:
        #         return mark_safe(str(self.img.path))
        #     else:
        #         return 'none'
        # display_img_path.short_description = 'Путь к изображению'
        # display_img_path.allow_tags = True


    def __str__(self):
        return str(self.id)


class Post(models.Model):
    title = models.TextField("Заголовок", max_length=500, unique=True)
    html = models.TextField("ХТМЛ")
    original_post = models.URLField(verbose_name="Источник", null=True) 
    text = models.TextField("Русский текст")
    channel = models.ForeignKey(
        "Channel",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Рубрика"
        )
    tags = models.ManyToManyField(Tag, verbose_name="Хештеги")
    pubdate = models.DateTimeField("Дата публикации", auto_now_add=True)
    rewritedate = models.DateTimeField("Дата редактирования", auto_now=True)
    slug = models.CharField(max_length=1000, null=True)
    img = models.ForeignKey(
        Image,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Первое изображение"
        )

    class Meta:
        ordering = ["-pubdate"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post-detail", args=[str(self.id)])

    def display_tag(self):
        return ', '.join([tag.name for tag in self.tags.all()[:]])
    display_tag.short_description = "Хештеги"

    def display_image(self):
        if self.img:
            return mark_safe('<img src="%s" width="96" height="96"></img>' % self.img.nice_x300_url(size=0))
        else:
            return 'none'
    display_image.short_description = 'Изображение'
    display_image.allow_tags = True


class Источник(models.Model):
    дата_создания = models.DateTimeField("Дата создания", default=timezone.now)
    дата_публикации = models.DateTimeField("Дата публикации", null=True)
    PUBLISHED = "Опубликован"
    CREATED = "Создан"
    STATUS = (
        (PUBLISHED, "PUBLISHED"),
        (CREATED, "CREATED"),
    )
    ссылка = models.URLField("Ссылка")
    powersubject = models.ForeignKey(
        Subject,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Канал"
        )
    статус = models.CharField(
        "Статус",
        max_length=15,
        choices=STATUS,
        null=False,
        default="Создан"    
    )
    
    def обновить(self):
        новые_ссылки = []
        ссылки_в_базе = self.objects.all()
        сслылки_для_добавления = []
        r = requests.get("http://curiosity.com/trendings/likes/topics/")
        text = r.text
        soup = BeautifulSoup(text, 'lxml')
        items = soup.find_all('a', {'class': 'topic-link'})
        for item in items:
            href = item.get('href')
            новые_ссылки.append(str('http://curiosity.com' + href))
        for сслыка in set(новые_ссылки).difference(ссылки_в_базе):
            сслылки_для_добавления.append(ссылка)
            self.objects.create(сслыка=сслыка)

    def __str__(self):
        return self.ссылка