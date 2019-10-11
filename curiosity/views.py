import sys
import logging
from urllib.parse import urlparse
from django.core.files import File
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Post, Tag, Channel, Image
from .worker.curiosity_one_post import django_db, draw


def get_logs():
    # PATH_TO_LOG = 'curiosity/static/curiosity/more-more-sting.log'
    fmt = logging.Formatter('%(asctime)s %(levelname)s %(module)s %(funcName)s %(message)s')

    # file_handler = logging.FileHandler(filename=PATH_TO_LOG)
    # file_handler.setFormatter(fmt)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(fmt)

    root_logger = logging.getLogger()

    # root_logger.addHandler(file_handler)
    root_logger.addHandler(stream_handler)

    root_logger.setLevel(logging.DEBUG)
    return root_logger


logger = get_logs()


def index(request):
    """Просмотр функции для главной страницы сайта."""

    # Сформировать подсчеты некоторых из основных объектов
    num_posts = Post.objects.all().count()
    num_channels = Channel.objects.all().count()

    # Опубликованные посты (status = 'a')
    num_pub = len([post.status for post in Post.objects.all() if post.status == "Опубликован"])
    num_new = len([post.status for post in Post.objects.all() if post.status == "Обнаружен"])
    # «Все ()» подразумевается по умолчанию.    
    num_tags = Tag.objects.count()

    # Количество посещений этой cnhfybws, поскольку, подсчитанных в переменной сеанса.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1

    context = {
        'num_new': num_new,
        'num_posts': num_posts,
        'num_channels': num_channels,
        'num_pub': num_pub,
        'num_tags': num_tags,
        'num_visits': num_visits,
    }

    # Рендер шаблон HTML index.html с данными в переменном контексте
    return render(request, 'curiosity/index.html', context=context)


def get_new_posts_of_file(request):
    Post.get_new_posts_of_file()
    return HttpResponseRedirect('/curiosity/')


def get_new_posts_of_network(request):
    Post.get_new_posts_of_network()
    return HttpResponseRedirect('/curiosity/')


def check_channel(channel, channel_en):
    if channel is None:
        return
    elif Channel.objects.get_or_create(name=channel, name_en=channel_en)[1]:
        channel = Channel.objects.get_or_create(name=channel, name_en=channel_en)[0]
        channel.save()
        return channel
    else:
        channel = Channel.objects.get_or_create(name=channel, name_en=channel_en)[0]
        return channel


def check_tags(tags, tags_en):
    tags_obj = []
    if tags is None:
        return
    else:
        for tag in tags and tag_en in tags_en:
            if Tag.objects.get_or_create(name=tag, name_en=tag_en)[1]:
                tag_obj = Tag.objects.get_or_create(name=tag, name_en=tag_en)[0]
                tag_obj.save()
                tags_obj.append(tag_obj)
            else:
                tag_obj = Tag.objects.get_or_create(name=tag, name_en=tag_en)[0]
                tags_obj.append(tag_obj)
    return tags_obj

 
def add_tags(post, tags):
    for tag in check_tags(tags):
        post.tags.add(tag)        


def add_image(post, img_href, channel, title):
    img_url = "https://dw8stlw9qt0iz.cloudfront.net/" + img_href[5] + ".png"
    name = urlparse(img_url).path.split('/')[-1]
    content = urllib.request.urlretrieve(img_url)
    draw_img_temp_path = draw(channel, title, img_path=content[0])
    file = File(open(draw_img_temp_path, "rb"))
    logger.info(f"Путь к временному изображению: {post.img.path}")
    post.img.save(name, file, save=True)
    try:
        logger.info(f"Облась в памяти для хранилища: {post.img.storage}")
    except Exception as err:
        logger.error(f"{err}")
    post.save()
    logger.info(f"Путь к сохраненному изображению: {post.img.path}")
    file.close()


def create_image(href, post):

    image = Image.objects.get_or_create(
        id=href[0].split('/')[len(href[0].split('/'))-1],
        urls_x300=", ".join([hr for hr in href if str("x300") in hr]),
        urls_x600=", ".join([hr for hr in href if str("x600") in hr])
        )[0]

    image.save()

    post.img = image

    post.save()


def updatedb(request):

    img_1_href, post_slug, tags_ru, channel_ru, title_ru, text_ru, html, href, channel, tags = django_db()

    post = Post.objects.get_or_create(title=title_ru,
                                      html=html,
                                      url=href,
                                      slug=post_slug,
                                      text=text_ru,
                                      channel=check_channel(channel=channel_ru, channel_en=channel),)[0]

    post.save()
    create_image(href=img_1_href, post=post)
    add_tags(post=post, tags=tags_ru)

    return HttpResponseRedirect('/curiosity/')