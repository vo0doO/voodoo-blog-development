import os
import re
import time
import sys
import requests
import vk_api
from PIL import Image, ImageFont, ImageDraw, ImageFilter, ImageOps
from bs4 import BeautifulSoup
import logging
from curiosity.models import Post, Tag, Channel
import re


# ПЕРЕМЕННЫЕ
HOW_POST_TO_PRINT = 5
VK_TOKEN = "9bfae56722ff872d603c6b0aa10c9c47f42fa00de836de4e47217e44c7f06259767efb6ee95c494303a8e"
PATH_TO_LOG = os.path.dirname(os.path.abspath(__file__)) + "/curiosity-to-vk.log"
PATH_MY_HREF = os.path.dirname(os.path.abspath(__file__)) + "/my_href.db"
PATH_TO_BACKUP_HREF = os.path.dirname(os.path.abspath(__file__)) + "/my_href_backup.db"
PATH_TO_POST = os.path.dirname(os.path.abspath(__file__)) + "/href-to-post.db"
PATH_TO_IMG_RESIZE = os.path.dirname(os.path.abspath(__file__)) + "/topics/IMG_RESIZE.png"
PATH_TO_IMG_ORIGINAL = os.path.dirname(os.path.abspath(__file__)) + "/topics/IMG_ORIGINAL.png"
# PATH_TO_IMG_1_COMPOSITE = os.path.dirname(os.path.abspath(__file__)) + "/topics/IMG_COMPOSITE.png"
PATH_TO_IMG_LOGO_PAINTER = os.path.dirname(os.path.abspath(__file__)) + "/desing/logo-painter.png"
PATH_TO_FONTS = os.path.dirname(os.path.abspath(__file__)) + "/topics/Roboto-Fonts/Roboto-Bold.ttf"
PATH_TO_IMG_BUTTON = os.path.dirname(os.path.abspath(__file__)) + "/Button.png"
VK_GROUP_ID = 181925964
UUID4_HEX_REGEX = re.compile('[0-9a-f]{12}4[0-9a-f]{3}[89ab][0-9a-f]{15}\Z', re.I)

# СОЗДАЕМ ЛОГГЕР
logger = logging.getLogger(__name__)


# СИНХРОНИЗАТОР ССЫЛОК
def change_href():
    href_new = []
    href_in_db = []
    href_to_post = []
    with open(PATH_MY_HREF) as database:
        for line in database:
            href_in_db.append(line.replace('\n', ''))
    r = requests.get("https://curiosity.com")
    text = r.text
    soup = BeautifulSoup(text, 'lxml')
    items = soup.find_all('a', {'class': 'topic-link'})
    for item in items:
        href = item.get('href')
        href_new.append(str('http://curiosity.com' + href))
    for href in set(href_new).difference(href_in_db):
        href_to_post.append(href)
    with open(PATH_MY_HREF, 'a') as f:
        for line in href_to_post[0:HOW_POST_TO_PRINT]:
            f.write(str(line) + '\n')
    with open(PATH_TO_POST, 'w') as h:
        for line in href_to_post[0:HOW_POST_TO_PRINT]:
            h.write(str(line) + '\n')


# ЧИТАТЕЛЬ БАЗЫ ССЫЛОК
def read_db(PATH_TO_POST):
    links = []
    with open(PATH_TO_POST, 'r') as f:
        link_list = f.readlines()
        for link in link_list:
            if str('\n') in str(link):
                link = str(link).replace('\n', '')
            links.append(str(link))
    return links


# СКАРПЕР ССЫЛКИ
def parser(href):
    # НАСТРАИВАЕМ ПАРСЕРА
    r = requests.get(href)
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


# ПЕРЕВОДЧИК ДАННЫХ
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
    logger.info("Переводчик выполнил свою работу")
    return tags_ru, channel_ru, title_ru, text_1_ru


# КРАУЛЕР ИЗОБРАЖЕНИЙ
def img_1_downloader(img_1_href, post_slug):
    if img_1_href is not None:
        img_url = "https://dw8stlw9qt0iz.cloudfront.net/" + img_1_href[35] + ".png"
        name = post_slug + ".png"
        res = requests.get("https://dw8stlw9qt0iz.cloudfront.net/" + img_1_href[35] + ".png", "b")
        with open(f"{os.getcwd()}/curiosity/static/curiosity/img/{post_slug}.png", 'wb') as zero:
            zero.write(res.content)
    else:
        logger.info("Ошибка загрузки изображения")
    logger.info("Скачены изображениея")


# ХУДОЖНИК
def draw(channel_ru, title_ru, img_path):
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


# ЖУРНАЛИСТ
def post(text_1_ru, tags_ru, video_1_data_scr, title_ru):
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


# ПОЛУЧЕНИЕ ЛОГОВ
def get_logs():
    fmt = logging.Formatter('%(asctime)s %(levelname)s %(module)s %(funcName)s %(message)s')

    file_handler = logging.FileHandler(filename=PATH_TO_LOG)
    file_handler.setFormatter(fmt)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(fmt)

    root_logger = logging.getLogger()

    root_logger.addHandler(file_handler)
    root_logger.addHandler(stream_handler)

    root_logger.setLevel(logging.INFO)
    return root_logger


def checkposts(myposts, hrefs):
    from urllib.parse import urlparse
    href_to_posts = []
    my_slugs = [post.slug for post in myposts]
    if len(myposts) == 0:
        return hrefs
    else:
        for href in hrefs:
            if urlparse(href).path.split('/')[len(urlparse(href).path.split('/'))-2] not in my_slugs:
                href_to_posts.append(href)
            else:
                logger.info(f"The post published: {urlparse(href).path.split('/')[len(urlparse(href).path.split('/'))-2]}")
        return href_to_posts


def django_db():
    # ПОЛУЧАЕМ ЛОГЕРА
    root_logger = get_logs()
    # ДЕКОРИРУЕМ ЛОГИ
    root_logger.info('='*100)

    hrefs = checkposts(Post.objects.all(), read_db(PATH_TO_BACKUP_HREF))

    logger.info(f"Доступно {len(hrefs)} новых постов.")

    for href in hrefs:
        post_slug = href.replace('http://curiosity.com/topics/', '').replace('/', '')
        img_1_href, channel, title, text_1, video_1_data_scr, tags, html = parser(href)
        tags_ru, channel_ru, title_ru, text_ru = translater(channel, title, text_1, tags)
        # img_1_downloader(img_1_href, post_slug)
        # draw(channel_ru, title_ru, post_slug)
        tags_ru = tags_ru.replace(" ", "")
        tags_ru = tags_ru.split("\n")
        tags_ru = [tag for tag in tags_ru if len(tag) >= 2]
        text_ru = text_ru.replace("\n\n\n", "\n", 1)
        return img_1_href, post_slug, tags_ru, channel_ru, title_ru, text_ru, html, href

    return



# Запуск скриптов
# def main():
#     change_href()
#     hrefs = read_db(PATH_TO_POST)
#     logger.info(f"Сейчас мы напишем {len(hrefs)} постов: ")
#     for count in hrefs:

#         try:
#             logger.info(msg=f"ПОСТ № {len(hrefs) - hrefs.index(str(count))}  {count.replace('http://curiosity.com/topics/', '').replace('/', '')}")
#             post_slug = count.replace('http://curiosity.com/topics/', '').replace('/', '')
#             img_1_href, channel, title, text_1, video_1_data_scr, tags = parser(count)
#             logger.info("Сканирование адреса законченно")
#             tags_ru, channel_ru, title_ru, text_1_ru = translater(channel, title, text_1, tags)
#             img_1_downloader(img_1_href)
#             draw(channel_ru, title_ru, post_slug)
#             logger.info("Художник намолевал")
#             post(text_1_ru, tags_ru, video_1_data_scr, title_ru)
#             logger.info("Пост опубликован")
#             with open("number_post.txt", 'w') as n:
#                 n.write(str(count))
#         except:
#             logger.exception(f"Ошибка на {count} посте")
#             continue
#         time.sleep(30);
