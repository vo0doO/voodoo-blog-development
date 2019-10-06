from curiosity import views
from django.urls import path


app_name = "curiosity"
urlpatterns = [
    path('', views.index, name='index'),
    path('updatedb/', views.updatedb, name='updatedb')
]