import os
import re
import uuid
import vk_api
import django
import requests
import platform
from django.db import models
from bs4 import BeautifulSoup
from django.urls import reverse
from django.utils import timezone
from urllib.parse import urlparse
from django.contrib.auth.models import User 
from django.http import HttpResponseRedirect
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


class PostAuthor(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    bio = models.TextField(max_length=400, help_text="Введите био подробности здесь.")
    
    class Meta:
        ordering = ["user","bio"]

    def get_absolute_url(self):
        """
        Возвращает URL для доступа конкретного экземпляра блог-автор.
        """
        return reverse('posts-by-author', args=[str(self.id)])

    def __str__(self):
        """
        Строка для представления объектной модели.
        """
        return self.user.username


class Post(models.Model):

    author = models.ForeignKey(PostAuthor, on_delete=models.SET_NULL, null=True, blank=True)
    comments = models
    title_en = models.CharField("Английский аголовок", max_length=500, unique=True, null=True)
    text_en = models.TextField("Английский текст", null=True)
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
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True, null=True)
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
        return reverse("post-detail", args=[str(self.slug)])

    def parser(self):
        # НАСТРАИВАЕМ ПАРСЕРА
        r = requests.get(self.url)
        html = r.text.encode("utf-8")
        soup = BeautifulSoup(html, "lxml")
        page = soup.find("div", {"class": "topic-page"})
        content_header = page.find_all("div", {"class": "image-header"})
        contents = page.find("div", {"class": ["topic-content", "content-items"]})
        content_item = contents.find_all("div", {"class": "content-item"})
        regexp_img_1 = re.compile(r'https://dw8stlw9qt0iz\.cloudfront\.net/(.*?)\.png\"')
        text = soup.findAll(lambda tag: tag.name == 'div' and tag.get('class') == ['embedded-text-content'])
        t = text[:]
        texts = [text.p.text for text in t]
        text_1 = ""
        count = 0
        max_index = len(texts) - 1
        while count <= max_index:
            text_1 += texts[count] + '\n' + '\n'
            count += 1
        # Головные данные
        for item in content_header:
            # ТЕГИ ТЕКСТ
            try:
                if page.find("div", {"class", "topic-tags"}).text is not None:
                    tags = page.find("div", {"class", "topic-tags"}).text
            except AttributeError:
                tags = None
            # ID 1-го изображения
            img_1_href = re.findall(regexp_img_1, item.find('style').text)
            # ID видеоролика
            try:
                video_1_data_scr = \
                    contents.find("div", {"class": "first-video"}).find("div", {"class": "module-video"}).find("div", {
                        "class": "js-media-player"})["data-src"]
            except Exception as e:
                logger.exception(msg=f"Ошибка парсера: ссылка на видео не найдена - {e}")
                video_1_data_scr = None
            # условия прохода если HTML топика с багами
            if item.find("div", {"class": "header-content"}).find('a') != None:
                # название канала
                channel = item.find("div", {"class": "header-content"}).find('a').text
                # заголовок топика
                title = item.find("div", {"class": "header-content"}).find('h1').text
            elif item.find("div", {"class": "header-content"}).find('a') == None:
                channel = item.find("div", {"class": "header-content"}).find('h5').text
                title = item.find("div", {"class": "header-content"}).find('h1').text
        try:
            return img_1_href, channel, title, text_1, video_1_data_scr, tags, html
        except Exception as e:
            logger.exception(msg=f"Ошибка парсера: {e}")
            return img_1_href, channel, title, text_1, video_1_data_scr, tags, html

    def img_1_downloader(self, img_1_href, post_slug):
        if img_1_href is not None:
            img_url = "https://dw8stlw9qt0iz.cloudfront.net/" + img_1_href[35] + ".png"
            name = post_slug + ".png"
            res = requests.get("https://dw8stlw9qt0iz.cloudfront.net/" + img_1_href[35] + ".png", "b")
            with open(f"{os.getcwd()}/curiosity/static/curiosity/img/{post_slug}.png", 'wb') as zero:
                zero.write(res.content)
        else:
            print("Ошибка загрузки изображения")

    def draw(self, channel_ru, title_ru, img_path):
        img_path_resize = img_path + "_resize.png"
        img_path_draws = img_path + "_draws.png"
        # НАЗВАНИЕ КАНАЛА
        channel = channel_ru.upper()
        # ЗАГОЛОВОК
        if len(title_ru) <= 70:
            title = title_ru
        else:
            titlelist = list(title_ru)
            titlelist.insert(70, '-')
            titlelist.insert(71, '\n')
            title = ''.join(titlelist)
        # ОБЛОЖКА ТОПИКА НА АНГЛ.
        img_composit = Image.open(img_path).convert("RGBA")
        _size_im_composit = (2560, 2048)
        img_composit = img_composit.resize(_size_im_composit, resample=0)
        # БАЗА, ОНА ЖЕ - ЛОГО_ПАИНТЕР
        logo_painter = Image.open(PATH_TO_IMG_LOGO_PAINTER).convert("RGBA")
        # ШРИФТЫ
        channel_font = ImageFont.truetype(PATH_TO_FONTS, 64)
        title_font = ImageFont.truetype(PATH_TO_FONTS, 64)
        # РАЗМЕР БЛОКА ТЕКСТА С НАЗВАН
        channel_size = channel_font.getsize(str(channel))
        # РАЗМЕР БЛОКА ТЕКСТА С НАЗВАНИЕМ КАНАЛА В КОРТЕЖЕ
        _size = (channel_size[0] + 20, channel_size[1] + 40)
        # НОВОЕ ИЗОБРАЖЕНИЕ ДЛЯ НАНЕСЕНИЯ ТЕКСТА С НАЗВАНИЕМ КАНАЛА
        channel_im = Image.open(PATH_TO_IMG_BUTTON).convert("RGBA")
        # ИЗМЕНЯЕМ РАЗМЕР ИЗОБРАЖЕНИЯ
        channel_img = channel_im.resize(_size, resample=0)
        # КИСТЬ для пустое ИЗОБРАЖЕНИЕ для нанесения текста с названием КАНАЛА
        channel_draw = ImageDraw.Draw(channel_img)
        # МЕТОД ПРОРИСОВКИ мультистрокового ТЕКСТА с названием канала на изобрание
        x = (_size[0] - channel_size[0]) / 2
        y = (_size[1] - channel_size[1]) / 2
        channel_draw.multiline_text((x, y), channel, font=channel_font, spacing=0, align="center")
        # ============================================== #
        # #########МОДИФИКАЦИЯ ИЗОБРАЖЕНИЯ############## #
        # ============================================== #
        # МОДИФИКАЦИЯ нижней части ОСНОВНОГО ИЗОБРАЖЕНИЯ #
        # ============================================== #
        box = (1, 2325, 2049, 2559)
        # ВЫРЕЗАЕМ
        text = img_composit.crop(box)
        # СОЗДАЕМ ФИЛТР
        gaus = ImageFilter.GaussianBlur(radius=20)
        # ПРИМЕНЯЕМ ФИЛТР К ВЫРЕЗКЕ
        textarea = text.filter(gaus)
        # УДАЛЯЕМ ГРАНИЦЫ
        ImageOps.crop(textarea)
        # ВСТАВЛЯЕМ ВЫРЕЗКУ НАЗАД
        img_composit.paste(textarea, (1, 2325))
        img_composit.save(img_path_resize)
        # КИСТЬ для ЗАГРУЗЧИКА
        logo_painter_draw = ImageDraw.Draw(logo_painter)
        # ПРОРИСОВКА канал загрузчик
        logo_painter.paste(channel_img, (27, 1750))
        # ПРОРИСОВКА заголовок на ЗАГРУЗЧИК ЛОГОТИПОВ
        logo_painter_draw.multiline_text((27, 1900), title, font=title_font, spacing=4, align="left")  # fill=(255,0,255,255)
        # СВЕДЕНИЕ СЛОЕВ обложки и загрузчика логотипов
        img_composite = Image.open(img_path_resize, mode='r').convert("RGBA")
        img_composite = Image.alpha_composite(img_composite, logo_painter)
        # СОХРАНЯЕМ РЕЗУЛЬТАТ - ГОТОВУЮ ОБЛОЖКУ ПОСТА в файл
        img_composite.save(img_path_draws)
        return img_path_draws

    def social_post(self, text_1_ru, tags_ru, video_1_data_scr, title_ru):
        # Аутинтификация
        # логин
        login, password = '89214447344', 'e31f567b'
        vk_session = vk_api.VkApi(login, password, api_version="5.67", app_id="6990349", client_secret="28fa7dcc28fa7dcc28fa7dcc692890d7c1228fa28fa7dcc74181bea3d7444b948bf5c47", scope=140488159)
        #vk_session = vk_api.VkApi(token=VK_TOKEN, scope=140488159)
        # проверка сессиии
        try:
            vk_session.auth()  # token_only=True
        except vk_api.AuthError as error_msg:
            logger.info(error_msg)
            return
        # получаем объект API
        vk = vk_session.get_api()
        # получаем файловый объект сессии используемый для загрузки
        upload = vk_api.VkUpload(vk_session)
        # получаем объект конкретной фотографии
        photo = upload.photo(
            PATH_TO_IMG_1_COMPOSITE,
            album_id=266719496 #266719496
            )
        # ССЫЛКА НА САЙТ
        #  ☀☀☀☀☀☀☀ 🌈🌈🌈🌈🌈🌈 ✨✨✨✨✨🇷🇺 💡 🇷🇺
        # ПОДГОТОВКА ПЕРЕМЕННЫХ ДЛЯ ПОСТА
        tags_ru = tags_ru.replace(" ", "")
        tag_to_post = tags_ru.replace("\n", "🇷🇺#", 2)
        text = text_1_ru.replace("\n\n\n", "\n", 1)
        text = text.replace("Есть много мест, чтобы быть любопытно, так что мы начали с любопытством путешествии в Instagram. Где твое любопытство возьмет тебя? Следуйте за нами!", "", 1)
        text = text.replace("Наши редакторы вникают в ТОП рассказы любопытства каждый день на подкаст, который меньше вашего коммутируют. Щелкните здесь, чтобы слушать и учиться — за несколько минут!", "", 1)
        text = text.replace("Получать рассказы в ваш почтовый ящик каждое утро. Подпишитесь на нашу здесь ежедневно по электронной почте.", "", 1)
        # ТЕКСТ СТАТЬИ ДЛЯ ПОСТА
        post_message = f"{tag_to_post} \n {text}"
        # ВИДОС
        if video_1_data_scr is not None:
            link = f"https://www.youtube.com/watch?v={video_1_data_scr}"
        else:
            link = ""
        vk.wall.post(
            owner_id=420341478, #vo0dooid 420341478
            friends_only=0,
            from_group=0,
            message=str(post_message[:]),
            attachments=f'photo{photo[0]["owner_id"]}_{photo[0]["id"]}, {link}')
        logger.info(f"НАЗВАНИЕ: {title_ru}" + "\n")

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

    def publish_post(self, request):
        img_1_href, channel_en, title_en, text_en, video_1_data_scr, tags_en, html=self.parser(self)
        tags_ru, channel_ru, title_ru, text_ru = Post.translater(
            channel=channel_en,
            title=title_en,
            text_1=text_en,
            tags=tags_en
            )
        self.author = request.user
        self.text_en = text_en
        self.title_en = title_en
        self.title = title_ru
        self.html = html
        self.text = text_ru,
        self.channel = self.check_channel(channel=channel_ru, channel_en=channel_en)
        self.save()
        self.create_image(self, href=img_1_href)
        self.add_tags(self, tags_ru=tags_ru, tags_en=tags_en)
        self.status = "Опубликован"
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
    
    @staticmethod
    def translater(channel, title, text_1, tags):
        # КАНАЛ
        channel = {
            "key": "trnsl.1.1.20170730T114755Z.994753b77b648f24.f3ed7d2f59fcb232c089a1a3328c0e0b900d4925",
            "text": f"{channel}.",
            'lang': 'en-ru',
            'format': 'plain'
        }
        # ЗАГОЛОВОК
        title = {
            "key": "trnsl.1.1.20170514T220842Z.5b2c14ecd7990670.3ccb355751262f1359f3c3ff0b9b7d5447ce39a1",
            "text": f"{title}.",
            'lang': 'en-ru',
            'format': 'plain'
        }
        # ТЕКСТ
        text_1 = {
            "key": "trnsl.1.1.20170514T220842Z.5b2c14ecd7990670.3ccb355751262f1359f3c3ff0b9b7d5447ce39a1",
            "text": f"{text_1}.",
            'lang': 'en-ru',
            'format': 'plain'
        }
        # ТЕГИ
        if tags is not None:
            tags = {
                "key": "trnsl.1.1.20170514T220842Z.5b2c14ecd7990670.3ccb355751262f1359f3c3ff0b9b7d5447ce39a1",
                "text": f"{tags}",
                'lang': 'en-ru',
                'format': 'plain'
            }
            # ТЕГИ
        else:
            tags = {
                "key": "trnsl.1.1.20170514T220842Z.5b2c14ecd7990670.3ccb355751262f1359f3c3ff0b9b7d5447ce39a1",
                "text": f"Любопытно",
                'lang': 'en-ru',
                'format': 'plain'
            }
        tags_ru = requests.get('https://translate.yandex.net/api/v1.5/tr.json/translate', params=tags).json()
        # ДЕЛАЕМ ЗАПРОС К ЯНДЕКС ПЕРЕВОДЧИКУ И СОХРАНЯЕМ ОТВЕТ
        channel_ru = requests.get('https://translate.yandex.net/api/v1.5/tr.json/translate', params=channel).json()
        # КАНАЛ
        title_ru = requests.get('https://translate.yandex.net/api/v1.5/tr.json/translate', params=title).json()
        # ЗАГОЛОВОК
        text_1_ru = requests.get('https://translate.yandex.net/api/v1.5/tr.json/translate', params=text_1).json()

        channel_ru = channel_ru['text'][0]
        title_ru = title_ru['text'][0]
        text_1_ru = text_1_ru['text'][0]
        tags_ru = tags_ru['text'][0]
        tags_ru = tags_ru.replace(" ", "")
        tags_ru = tags_ru.split("\n")
        tags_ru = [tag for tag in tags_ru if len(tag) >= 2]
        text_ru = text_ru.replace("\n\n\n", "\n", 1)
        logger.info("Переводчик выполнил свою работу")
        return tags_ru, channel_ru, title_ru, text_1_ru

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
    def get_new_posts_of_file(*args, **kwargs):
        my_url = [post.url for post in Post.objects.all()]
        with open('D:\Projects\py\myblog-development\curiosity\worker\my_href_backup.db', 'r') as f:
            new_url_list = f.readlines()
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

    @property
    def is_readypub(self):
        if self.text and self.title and self.img:
            return True
        return False

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_date"]
        permissions = (('can_mark_returned', 'Can mark returned'),)

    def clean(self) -> None:

        try:
            if self.author is not None:
                print(f"{author} is author field")
            else:
                raise ValidationError(f"{author} field is not Validate")

            if self.title is not None:
                print(f"{title} is title field")
            else:
                raise ValidationError(f"{title} field is not Validate")

            if self.text is not None:
                print(f"{text} is text field")
            else:
                raise ValidationError(f"{text} field is not Validate")

            if self.title is not None:
                print(f"{title} is title field")
            else:
                raise ValidationError(f"{title} field is not Validate")

            if self.html is not None:
                print(f"{html} is html field")
            else:
                raise ValidationError(f"{html} field is not Validate")

            if self.url is not None:
                print(f"{url} is url field")
            else:
                raise ValidationError(f"{url} field is not Validate")

            if self.text is not None:
                print(f"{text} is text field")
            else:
                raise ValidationError(f"{text} field is not Validate")

            if self.channel is not None:
                print(f"{channel} is channel field")
            else:
                raise ValidationError(f"{channel} field is not Validate")

            if self.tags is not None:
                print(f"{tags} is tags field")
            else:
                raise ValidationError(f"{tags} field is not Validate")

            if self.created is not None:
                print(f"{created} is created field")
            else:
                raise ValidationError(f"{created} field is not Validate")

            if self.pub is not None:
                print(f"{pub} is pub field")
            else:
                raise ValidationError(f"{pub} field is not Validate")

            if self.rewrite is not None:
                print(f"{rewrite} is rewrite field")
            else:
                raise ValidationError(f"{rewrite} field is not Validate")

            if self.slug is not None:
                print(f"{slug} is slug field")
            else:
                raise ValidationError(f"{slug} field is not Validate")

            if self.img is not None:
                print(f"{img} is img field")
            else:
                raise ValidationError(f"{img} field is not Validate")
        except Exception as error:
            pritn(f"Error: {error.args}")
            self.publish_post(self, request)


class PostComment(models.Model):
    """
    Модель, представляющая комментарий против блоге.
    """
    description = models.TextField(max_length=1000, help_text="Enter comment about blog here.")
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
      # Foreign Key used because BlogComment can only have one author/User, but users can have multiple comments
    post_date = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    
    class Meta:
        ordering = ["post_date"]

    def __str__(self):
        """
       Строка для представления объектной модели.
        """
        len_title=75
        if len(self.description)>len_title:
            titlestring=self.description[:len_title] + '...'
        else:
            titlestring=self.description
        return titlestring
