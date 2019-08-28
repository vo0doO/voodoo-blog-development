from django.urls import path
from . import views
import uuid

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('answer/<pk>', views.answer_detail, name='answer_detail'),
    path('answer/new/', views.answer_new, name='answer_new'),
    path('procedury', views.procedury, name='procedury')
]