import os
import re
import time
import sys
import requests
import vk_api
from PIL import Image, ImageFont, ImageDraw, ImageFilter, ImageOps
from bs4 import BeautifulSoup
import logging


# ПЕРЕМЕННЫЕ
HOW_POST_TO_PRINT = 1
VK_TOKEN = "9bfae56722ff872d603c6b0aa10c9c47f42fa00de836de4e47217e44c7f06259767efb6ee95c494303a8e"
PATH_TO_LOG = os.path.dirname(os.path.abspath(__file__)) + "/curiosity-to-vk.log"
PATH_MY_HREF = os.path.dirname(os.path.abspath(__file__)) + "/my_href.db"
PATH_TO_POST = os.path.dirname(os.path.abspath(__file__)) + "/href-to-post.db"
PATH_TO_IMG_RESIZE = os.path.dirname(os.path.abspath(__file__)) + "/topics/IMG_RESIZE.png"
PATH_TO_IMG_ORIGINAL = os.path.dirname(os.path.abspath(__file__)) + "/topics/IMG_ORIGINAL.png"
PATH_TO_IMG_1_COMPOSITE = os.path.dirname(os.path.abspath(__file__)) + "/topics/IMG_COMPOSITE.png"
PATH_TO_IMG_LOGO_PAINTER = os.path.dirname(os.path.abspath(__file__)) + "/desing/logo-painter.png"
PATH_TO_FONTS = os.path.dirname(os.path.abspath(__file__)) + "/topics/Roboto-Fonts/Roboto-Bold.ttf"
PATH_TO_IMG_BUTTON = os.path.dirname(os.path.abspath(__file__)) + "/Button.png"


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
    with open(PATH_TO_POST, 'r') as f:
        links = f.readlines()
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
        except:
            video_1_data_scr = None
            print("ссылка на видео не найдена")
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
        CACHE = [href, img_1_href, channel, title, text_1, video_1_data_scr, tags]
        return img_1_href, channel, title, text_1, video_1_data_scr, tags
    except:
        return img_1_href, channel, title, text_1, video_1_data_scr, tags
        logger.exception(msg='Ошибка парсера:')


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
    print("Переводчик выполнил свою работу")
    return tags_ru, channel_ru, title_ru, text_1_ru


# КРАУЛЕР ИЗОБРАЖЕНИЙ
def img_1_downloader(img_1_href):
    if img_1_href is not None:
        res = requests.get("https://dw8stlw9qt0iz.cloudfront.net/" + img_1_href[35] + ".png", "b")
        with open(PATH_TO_IMG_ORIGINAL, 'wb') as zero:
            zero.write(res.content)
    else:
        print("Ошибка загрузки изображения")
    print("Скачены изображениея")


# ХУДОЖНИК
def draw(channel_ru, title_ru):
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
    img_composit = Image.open(PATH_TO_IMG_ORIGINAL).convert("RGBA")
    _size_im_composit = (2560, 2048)
    img_composit = img_composit.resize(_size_im_composit, resample=0)
    # БАЗА, ОНА ЖЕ - ЛОГО_ПАИНТЕР
    logo_painter = Image.open(PATH_TO_IMG_LOGO_PAINTER).convert(
        "RGBA")
    #logo_painter = logo_painter.resize(_size_im_composit, resample=0)
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
    '''
    # ========================
    # #########МОДИФИКАЦИЯ ИЗОБРАЖЕНИЯ#######
    # =========================
    # МОДИФИКАЦИЯ нижней части ОСНОВНОГО ИЗОБРАЖЕНИЯ
    '''
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
    img_composit.save(PATH_TO_IMG_RESIZE)
    # КИСТЬ для ЗАГРУЗЧИКА
    logo_painter_draw = ImageDraw.Draw(logo_painter)
    # ПРОРИСОВКА канал загрузчик
    logo_painter.paste(channel_img, (27, 1750))
    # ПРОРИСОВКА заголовок на ЗАГРУЗЧИК ЛОГОТИПОВ
    logo_painter_draw.multiline_text((27, 1900), title, font=title_font, spacing=4,
                                     align="left")  # fill=(255,0,255,255)
    # МОДИФИКАЦИЯ нижней части ОСНОВНОГО ИЗОБРАЖЕНИЯ
    # ВЫРЕЗАЕМ
    #img_composits = Image.open(
        #"E:/fo_DESK/curiosity-to-vk/topics/0-img-" + str(1) + ".png", mode='b').convert("RGBA")
    #logo_box = (1, 70, 2000, 70)
    #logob = img_composits.crop(logo_box)
    #gaus = ImageFilter.GaussianBlur(radius=20)
    # ЗАКАТЫВАЕМ ПОЛУЧЕНЫЙ КОМПОТ
    #img_composits.save("E:/fo_DESK/curiosity-to-vk/topics/0-img-" + str(1) + ".png")
    # СВЕДЕНИЕ СЛОЕВ обложки и загрузчика логотипов
    img_composite = Image.open(PATH_TO_IMG_RESIZE, mode='r').convert("RGBA")
    img_composite = Image.alpha_composite(img_composite, logo_painter)
    # СОХРАНЯЕМ РЕЗУЛЬТАТ - ГОТОВУЮ ОБЛОЖКУ ПОСТА в файл
    img_composite.save(PATH_TO_IMG_1_COMPOSITE)


# ЖУРНАЛИСТ
def post(text_1_ru, tags_ru, video_1_data_scr, title_ru):
    # Аутинтификация
    # логин
    login, password = '89214447344', 'e31f567b'
    vk_session = vk_api.VkApi(login, password, api_version="5.67", app_id="6990349", client_secret="28fa7dcc28fa7dcc28fa7dcc692890d7c1228fa28fa7dcc74181bea3d7444b948bf5c47", scope=140492191)
    # проверка сессиии
    try:
        vk_session.auth()  # token_only=True
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return
    # получаем объект API
    vk = vk_session.get_api()
    # получаем файловый объект сессии используемый для загрузки
    upload = vk_api.VkUpload(vk_session)
    # получаем объект конкретной фотографии
    try:
        photo = upload.photo(
            PATH_TO_IMG_1_COMPOSITE,
            album_id=248018572)
    except:
        photo = None
        print("Фото не загруженно")
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
        owner_id=279286486,
        friends_only=0,
        from_group=0,
        message=str(post_message[:]),
        attachments=f'photo{photo[0]["owner_id"]}_{photo[0]["id"]}, {link}')
    print(f"НАЗВАНИЕ: {title_ru}" + "\n")


# TODO: НАСТРОИТЬ работу с базой данных FIREBASE !!!!!!!!!!!
def database():
    """
    config = {
        "apiKey": "AIzaSyD6EzxDobegHGvkorLEle6OBt_RNedkD0g",
        "authDomain": "project-3931781304531690229.firebaseapp.com",
        "databaseURL": "https://project-3931781304531690229.firebaseio.com",
        "projectId": "project-3931781304531690229",
        "storageBucket": "project-3931781304531690229.appspot.com",
        "type": "service_account",
        "project_id": "project-3931781304531690229",
        "private_key_id": "fa36c163c3267295a17d6c34a7bbfb9fbb7fb860",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDH+ULfO0USH5/e\n8W274zuSjKMySBIJxU14tB1C+Sl4QREeMbndzflcnJ+HnRDNyvDL5Y9iaiHC+5Ao\nqdPJigr4ggR/jXZ7BMsAEcVVqyzzFZmnqhAdX//uxzjJQZFe8EdANdArhUHMWNr5\nWqY3zG27IqpxRb/75UevY3rWhiWiaIjSyCprNOhs1n16FG1Tjlgi1tG9C8F335qK\nAYiW1FhEZKYqDe82AZSTWwqx/hVl4D+m4BRpmvwbVdJY6cNqWKYUn7HcptmdpSon\nNLX5YxB02ATj1N9jjxzYxaw+msL0oN9ad1/2uzwl1CwdBVRpRGVl3gw6qAxgkTiR\ntExt33T5AgMBAAECggEBAJHiE5jKok7gZz67HfSNhu4YTw3ladNa7nN54kbzgf9K\naHSAjjlzg9C+KdtDB/k5bYUxyPJgvpSB9N7VVb2XSP2VzDZJOv/vtTAtxqoCoF4N\nifS4qdzkJc9J4vFfNe/ulewP1feJ1UCAKe7y5IOcTQjR90l/OtlGoI8goYJShq39\nDoEvp7oSQ3yy3WXSj+WwFrLPz79eLpFymw3WdJ1PRi2y2/ls+wLe5ostEG+FD3kq\ndGDOXXB+FJPJuJrODf6m9qPlxTQkWEXhMYMpMgfKWiAOKhNYYJQ4IpJLSXu4H3WY\ncVPaGRE1df9lrq1yBS35aWzeortebhWrlNKLHSUS4gECgYEA5D28n3NtSNYYhJhO\nLbvXvt7k80RyB+n/bZnX3U42NFrLdMt2yrB59MuDKkgKZubBZMBAZu6FDo6wC/6r\nSRbB30a3KoNlXhLeOGNGRqYLrJBL76Oxt0Ekm68nRdQEGbUUKza5hNoKJLnwBzdD\nazgUBc2gdncfw0xYdrKZ8QNhwpkCgYEA4EtrYk6b3ll2hVaWyZEYXA7upz+24A4k\neafLKMNP3tr0HU9V6VVcZRK72mRrAeBGAoSDm5/Mgvk8XQwr52/zvuV8yim1wmGd\nR1mpYGGSWBFaMxPwSgaBIOhDG0a3HSzfoTGXbUig0WaquMXXOrLk1b8HSBHPMWwR\n5Dm5LJAXIWECgYBS1ZkkYXbzLUh+ruwIqxjU2/5Jz7h26NTcCS6P0ffYLm+Sttkp\nHL1WO5oh+T1VNUBQ+XkmIkDGFMENyWKOxySbjQWi90cNylk+K8FwmIi6GzCEC2vP\nL2RC4GGndRf74H0uZdEUxzFRPO5BICxmuFaD+KnY9MjhT0733UADeY+8WQKBgQDG\nEnRTTV4ifljHKY9hk6uyaFFjC0YhGPwnHwGvDsPy5uLbG1ugAgzlCSUxmKpS7s6E\nnKdogDbnltgyx3PiHyBefWS1Vx42+WMeRlToU2IcOb6xCrORe6r+932DkfBVaHJY\ndGXoUVILeiHbqIMISEEDbX4tq+SQHYKzTDJ14w06IQKBgDZFDIVgk4v81yH0M+oe\nJ1oDUpFj//wVWfuOjalR/+udBIIVJXILchm6rVHOnTEWmvxFZCcD7Zxhy5pEGSDg\nHM/pHOPth8vh5qquEH+Ji613bp/VXVysN37xkpa23fhxSgankqbFiJoxpqOhgWYe\nxgKAzkt34Fug8XYO+hDAbL3X\n-----END PRIVATE KEY-----\n",
        "client_email": "firebase-adminsdk-alb7j@project-3931781304531690229.iam.gserviceaccount.com",
        "client_id": "105042264485843483839",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://accounts.google.com/o/oauth2/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-alb7j%40project-3931781304531690229.iam.gserviceaccount.com",
        "serviceAccount": "E:/fo_DESK/curiosity-to-vk/kirsanov-dot-com-e615c6a21595.json"
    }
    # инициализация базы
    firebase = pyrebase.initialize_app(config)
    # Получить ссылку на службу авторизации
    auth = firebase.auth()  # uid = 'some-uid'; custom_token = auth.create_custom_token(uid)
    # Зарегистрировать пользователя в базе
    user = auth.sign_in_with_email_and_password("danilakirsanovspb@gmail.com", "Nhb1,e2yfk3$")
    # Получить ссылку на службу базы данных
    return firebase.database()
"""


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

    root_logger.setLevel(logging.DEBUG)
    return root_logger


# Запуск скриптов
def main():

    change_href()
    # db = database()  ##TODO: НАСТРОИТЬ FIREBASE !!!!!!!!!!!
    hrefs = read_db(PATH_TO_POST)
    logger.info(f"Сейчас мы напишем {len(hrefs)} постов: ")
    for count in hrefs:

        try:
            logger.info(msg=f"ПОСТ № {len(hrefs) - hrefs.index(str(count))}  {count.replace('http://curiosity.com/topics/', '')}")
            img_1_href, channel, title, text_1, video_1_data_scr, tags = parser(count)
            print("Сканирование адреса законченно")
            tags_ru, channel_ru, title_ru, text_1_ru = translater(channel, title, text_1, tags)
            img_1_downloader(img_1_href)
            draw(channel_ru, title_ru)
            print("Художник намолевал")
            post(text_1_ru, tags_ru, video_1_data_scr, title_ru)
            print("Пост опубликован")
            with open("number_post.txt", 'w') as n:
                n.write(str(count))
        except:
            logger.exception(f"Ошибка на {count} посте")
            continue
        #try:
        #    Topic = collections.namedtuple("Topic", f"id img_1_href channel title text_1 video_1_data_scr tags channel_ru title_ru tags_ru text_1_ru")
        #    TOPIC = Topic(db.generate_key(), img_1_href[-1], channel, title, text_1, video_1_data_scr, tags, channel_ru, title_ru, tags_ru, text_1_ru)
        #    json.dump(json.dumps(TOPIC._asdict()), open('posts-firebase.json', 'a+b'), indent=4)
        #    data = {"curiosity/topics/"+str(count.replace('http://curiosity.com/topics/', '').replace('/\n', '')):
        #            json.dumps(TOPIC._asdict(), indent=4)
        #            };
        #    db.update(data);
        #    print(f"Информация записана в базу данных")
        # except: print(f"Ошиюка при записи в базу данных")
        time.sleep(30);


if __name__ == "__main__":
    post("del", "del", "del", "del")
    # ПОЛУЧАЕМ ЛОГЕРА
    root_logger = get_logs()
    # ДЕКОРИРУЕМ ЛОГИ
    root_logger.debug('='*100)
    # ВЫПОЛНЯЕМ ГЛАВНЫЙ СКРИПТ
    main()
    # ДЕКОРИРУЕМ ЛОГИ
    root_logger.debug('='*100)