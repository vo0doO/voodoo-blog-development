from django.urls import path
from . import views


app_name = "blog"
urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    # path('answer/new', views.answer_new, name='answer_new'),
    # path('answer/<pk>/final/', views.final, name='final'),
    # path('procedury', views.procedury, name='procedury'),
    # path('test', views.test, name='test'),
    path('answer/add', views.AnswerCreate.as_view(), name='answer-add'),
    path('answer/<uuid:pk>/', views.AnswerUpdate.as_view(), name='answer-update'),
    path('answer/<uuid:pk>/result/', views.AnswerResult.as_view(), name='answer-result'),
    path('answer/list/', views.AnswerListView.as_view(), name="answer_list"),
]