import os
import uuid
import django
import requests
import platform
from django.db import models
from bs4 import BeautifulSoup
from django.urls import reverse
from django.utils import timezone
from urllib.parse import urlparse
from django.utils.safestring import mark_safe
from django.core.files.storage import FileSystemStorage


class Log(models.Model):
    text = models.TextField("Текст", max_length=5000, null=True)
    created_at = models.DateTimeField("Дата обнаружения", auto_now=False, default=django.utils.timezone.now, blank=True)

    def __str__(self):
        return self.text


class Channel(models.Model):
    name = models.CharField("Русское название", null=True, max_length=250, unique=True)
    name_en = models.CharField("Английское название", null=True, max_length=250, unique=True)
    created_date = models.DateTimeField("Даты создания", default=django.utils.timezone.now, blank=True)
    like = models.PositiveIntegerField("Лайк", default=0)

    def __str__(self):
        return self.name.capitalize()


class Tag(models.Model):
    name = models.CharField("Русское название", null=True, max_length=250, unique=True)
    name_en = models.CharField("Английское название", null=True, max_length=250, unique=True)
    created_date = models.DateTimeField("Даты создания", default=django.utils.timezone.now, blank=True)
    like = models.PositiveIntegerField("Лайк", default=0)

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
    title = models.CharField("Заголовок", max_length=500, unique=True, null=True)
    html = models.TextField("ХТМЛ", null=True)
    url = models.URLField(verbose_name="Источник", null=True) 
    text = models.TextField("Русский текст", null=True)
    channel = models.ForeignKey(
        "Channel",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Рубрика"
        )
    tags = models.ManyToManyField(Tag, verbose_name="Хештеги")
    created_date = models.DateTimeField("Дата обнаружения", auto_now=False, default=django.utils.timezone.now, blank=True)
    pub_date = models.DateTimeField("Дата публикации", null=True)
    rewrite_date = models.DateTimeField("Дата редактирования", null=True, auto_now=True,)
    slug = models.SlugField(max_length=255, null=True, unique=True)
    img = models.ForeignKey(
        Image,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Первое изображение"
        )
    FINDED = "Обнаружен"
    PUBLISHED = "Опубликован"
    STATUS = (
        (FINDED, "FINDED"),
        (PUBLISHED, "PUBLISHED"),
    )
    status = models.CharField(
        "Статус",
        max_length=15,
        choices=STATUS,
        null=False,
        default="Обнаружен"    
    )

    def get_absolute_url(self):
        return reverse("post-detail", args=[str(self.id)])

    @staticmethod
    def create_new_post(new_url):
        my_url = [post.url for post in Post.objects.all()]
        if "/http://" in new_url:
            idx = new_url.index("/http://")
            new_url = new_url[0:idx]
        else:
            new_url = new_url
        try:
            new_url.replace('\n', '')
            if new_url in my_url:
                duble_count = duble_count + 1
                return Post.objects.get(url=new_url)
            elif new_url not in my_url:
                url = urlparse(new_url, allow_fragments=True)
                slug = url.path.replace('topics/', '')
                if "http" in slug:
                    idx = slug.index("http://")
                    slug = slug[0:idx]
                else:
                    slug = slug
                if Post.objects.get_or_create(slug=slug)[1]:
                    post = Post.objects.get_or_create(slug=slug)[0]
                    post.url = url.geturl()
                    log = Log.objects.create(text=f"Обнаружен пост {post.slug}")
                    log.save()
                    post.save()
                else:
                    post = Post.objects.get(slug=slug)
                    post.url = url.geturl()
                    post.save()
                    duble_count = duble_count + 1
                    return post
            else:
                log_err_2 = Log.objects.create(text=f"Ошибка: Что-то пошло не так...")
                log_err_2.save()
        except Exception as err:
            log = Log.objects.create(text=f"Ошибка: {err[:500]}")
            log.save()
        log = Log.objects.create(text=f"Обнаруженно {len(list(Post.objects.all())) - len(list(my_url))} новых постов")
        log.save()

    @staticmethod
    def get_new_posts_of_file():
        my_url = [post.url for post in Post.objects.all()]
    
        with open('D:\Projects\py\myblog-development\curiosity\worker\my_href_backup.db', 'r') as f:
            new_url_list = f.readlines()
            duble_count = 0
            for new_url in new_url_list:
                Post.create_new_post(new_url=new_url)

    @staticmethod
    def get_new_posts_of_network():
        html_path_list = [
            "D:\Projects\py\myblog-development\curiosity\static\curiosity\html\offbeat-adventure.html"
        ]
        my_url = [post.url for post in Post.objects.all()]
        new_url = []

        # r = requests.get("http://curiosity.com/trendings/likes/topics/")
        # text = r.text

        def get_html_of_file(path):
            with open(path, 'r') as html:
                text = html.read()
                return text

        for path in html_path_list:
            text = get_html_of_file(path)
            soup = BeautifulSoup(text, 'lxml')
            items = soup.find_all('a', {'class': 'topic-link'})
            for item in items:
                href = item.get('href')
                new_url.append(str('http://curiosity.com' + href))
            for new_url in set(new_url).difference(set(my_url)):
                Post.create_new_post(new_url=new_url)

    def check_channel(self, channel, channel_en):
        if channel is None:
            return
        elif channel_en is None:
            return
        elif Channel.objects.get_or_create(name=channel, name_en=channel_en)[1]:
            channel = Channel.objects.get_or_create(name=channel, name_en=channel_en)[0]
            channel.save()
            return channel
        else:
            channel = Channel.objects.get_or_create(name=channel, name_en=channel_en)[0]
            return channel

    def check_tags(self, tags, tags_en):
        tags_obj = []
        if tags is None:
            return
        elif tags_en is None:
            return
        else:
            for tag, tag_en in tags, tags_en:
                if Tag.objects.get_or_create(name=tag, name_en=tag_en)[1]:
                    tag_obj = Tag.objects.get_or_create(name=tag, name_en=tag_en)[0]
                    tag_obj.save()
                    tags_obj.append(tag_obj)
                else:
                    tag_obj = Tag.objects.get_or_create(name=tag, name_en=tag_en)[0]
                    tags_obj.append(tag_obj)
        return tags_obj

    def add_tags(self, tags_ru, tags_en):
        for tag in self.check_tags(self, tags=tags_ru, tags_en=tags_en):
            self.tags.add(tag) 

    def add_image(self, img_href, channel, title):
        img_url = "https://dw8stlw9qt0iz.cloudfront.net/" + img_href[5] + ".png"
        name = urlparse(img_url).path.split('/')[-1]
        content = urllib.request.urlretrieve(img_url)
        draw_img_temp_path = draw(channel, title, img_path=content[0])
        file = File(open(draw_img_temp_path, "rb"))
        logger.info(f"Путь к временному изображению: {post.img.path}")
        self.img.save(name, file, save=True)
        try:
            logger.info(f"Облась в памяти для хранилища: {post.img.storage}")
        except Exception as err:
            logger.error(f"{err}")
        self.save()
        logger.info(f"Путь к сохраненному изображению: {post.img.path}")
        self.close()

    def create_image(self, href):
        image = Image.objects.get_or_create(
            id=href[0].split('/')[len(href[0].split('/'))-1],
            urls_x300=", ".join([hr for hr in href if str("x300") in hr]),
            urls_x600=", ".join([hr for hr in href if str("x600") in hr])
            )[0]
        image.save()
        self.img = image
        self.save()

    def publish_post(self):
        img_1_href, post_slug, tags_ru, channel_ru, title_ru, text_ru, html, href, channel_en, tags_en = django_db()
        self.title = title_ru
        self.html = html
        self.text = text_ru,
        self.channel = self.check_channel(channel=channel_ru, channel_en=channel_en)
        self.save()
        self.create_image(self, href=img_1_href)
        self.add_tags(self, tags_ru=tags_ru, tags_en=tags_en)
        self.save()
        return HttpResponseRedirect('/curiosity/')

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

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_date"]
