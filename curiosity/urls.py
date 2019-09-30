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
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_URL)