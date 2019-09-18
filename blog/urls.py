from django.urls import path
from . import views


app_name = "blog"
urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('answer/add', views.AnswerCreate.as_view(), name='answer_add'),
    path('answer/<uuid:pk>/', views.AnswerDetail.as_view(), name='answer_detail'),
    path('answer/<uuid:pk>/update/', views.AnswerUpdate.as_view(), name='answer_update'),
    path('answer/list/', views.AnswerListView.as_view(), name="answer_list")
]

    # path('answer/new', views.answer_new, name='answer_new'),
    # path('answer/<pk>/final/', views.final, name='final'),
    # path('procedury', views.procedury, name='procedury'),
    # path('test', views.test, name='test'),