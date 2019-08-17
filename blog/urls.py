from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('', views.get_client_ip, name='get_client_ip'),
    path('client-ip/', views.get_client_ip, name='get_client_ip')
]