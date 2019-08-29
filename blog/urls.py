from django.urls import path
from . import views


app_name = "blog"
urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('answer/new/', views.answer_new, name='answer_new'),
    path('answer/<pk>/', views.final, name='final'),
    path('question/latest/', views.questions_latest, name='questions_latest'),
    path('question/<int:question_id>/', views.detail, name='detail'),
    path('question/<int:question_id>/results/', views.results, name='results'),
    path('question/<int:question_id>/vote/', views.vote, name='vote')
]