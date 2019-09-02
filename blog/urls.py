from django.urls import path
from . import views


app_name = "blog"


urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('answer/new/', views.answer_new, name='answer_new'),
    path('answer/<pk>', views.final, name='final'),
    path('procedury', views.procedury, name='procedury'),
    path('test', views.test, name='test')
]