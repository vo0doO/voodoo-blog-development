# coding=utf-8
"""myblog URL Configuration

Список `urlpatterns` направляет URL-адреса к представлениям. Для получения дополнительной информации, пожалуйста, смотрите:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Примеры:
Функциональные представления
    1. Добавить импорт: из представлений импорта my_app
    2. Добавьте URL в urlpatterns:  path('', views.home, name='home')
Основанные на классе представления
    1. Добавить импорт: из other_app.views import Home
    2. Добавьте URL в urlpatterns:  path('', Home.as_view(), name='home')
Включая другой URLconf
    1. Импортируйте include() function: from django.urls import include, path
    2. Добавить URL-адрес в urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('curiosity/', include('curiosity.urls'))
]