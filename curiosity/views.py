from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from .models import Post, Tag, Channel
from .worker.curiosity_one_post import django_db, logger, get_logs
import urllib
from urllib.parse import urlparse
from django.core.files import File


def updatedb(request):
    # ПОЛУЧАЕМ ЛОГЕРА
    root_logger = get_logs()
    # ДЕКОРИРУЕМ ЛОГИ
    root_logger.info('='*100)
    # ДЕКОРИРУЕМ ЛОГИ
    root_logger.info('='*100)

    img_1_href, post_slug, tags_ru, channel_ru, title_ru, text_ru = django_db()
    post = Post.objects.get_or_create(title=title_ru, slug = post_slug,
                text = text_ru, channel=Channel.objects.get(name=channel_ru))

    for tag in tags_ru:
        try:
            tag = Tag.objects.get(name=tag)
            post.tags.add(Tag.objects.get(name=tag))
        except Exception as err:
            otag = Tag.objects.create(name=tag)
            otag.save()
            post.tags.add(otag)
    img_url = "https://dw8stlw9qt0iz.cloudfront.net/" + img_1_href[35] + ".png"
    name = urlparse(img_url).path.split('/')[-1]
    content = urllib.request.urlretrieve(img_url)
    post.image.save(name, File(open(content[0])), save=True)
    post.save()
    # except Exception as err:
    #     logger.info(f"Ошибка при создании поста: {err}")