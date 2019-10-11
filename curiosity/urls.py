from curiosity import views
from django.urls import path


app_name = "curiosity"
urlpatterns = [
    path('', views.index, name='index'),
    path('posts/get/file/', views.get_new_posts_of_file, name='get_new_posts_of_file'),
    path('posts/get/net/', views.get_new_posts_of_network, name='get_new_posts_of_network'),
    path('updatedb/', views.updatedb, name='updatedb'),
]