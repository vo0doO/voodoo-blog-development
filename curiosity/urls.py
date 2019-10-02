from django.urls import path
from . import views
# DEBUG
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings

app_name = "curiosity"
urlpatterns = [
    path('updatedb', views.updatedb, name='updatedb')
]