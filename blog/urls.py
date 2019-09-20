from django.urls import path
from . import views


app_name = "blog"
urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('answer/add', views.AnswerCreate.as_view(), name='answer_add'),
    path('answer/<uuid:pk>/', views.AnswerDetail.as_view(), name='answer_detail'),
    path('answer/<uuid:pk>/update/', views.AnswerUpdate.as_view(), name='answer_update'),
    path('answer/list/', views.AnswerListView.as_view(), name="answer_list"),
    path('procedury', views.procedury, name='procedury'),
    path('regulation', views.regulation, name='regulation'),
    path('consent', views.consent, name='consent')
]