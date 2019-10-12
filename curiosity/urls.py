from curiosity import views
from django.urls import path


app_name = "curiosity"

urlpatterns = [
    path('', views.index, name='index'),
    path('posts/list/', views.PostListView.as_view(), name='post-list'),
    path('posts/create/', views.PostCreateView.as_view(), name='post-create'),
    path('posts/<slug:slug>/', views.PostDetailView.as_view(), name="post-detail"),
    path('posts/<slug:slug>/update/', views.PostUpdateView.as_view(), name="post-change"),
    path('posts/<slug:slug>/delete/', views.PostDeleteView.as_view(), name="post-delete"),
]


urlpatterns += [
    path('authors/list/', views.PostAuthorListView.as_view(), name='author-list'),
    path('authors/create/', views.PostAuthorCreateView.as_view(), name='author-create'),
    path('authors/<pk>/', views.PostAuthorDetailView.as_view(), name="author-detail"),
    path('authors/<pk>/update/', views.PostAuthorUpdateView.as_view(), name="author-change"),
    path('authors/<pk>/delete/', views.PostAuthorDeleteView.as_view(), name="author-delete"),
]

urlpatterns += [
    path('tags/list/', views.TagListView.as_view(), name='tag-list'),
    path('tags/create/', views.TagCreateView.as_view(), name='tag-create'),
    path('tags/<pk>/', views.TagDetailView.as_view(), name="tag-detail"),
    path('tags/<pk>/update/', views.TagUpdateView.as_view(), name="tag-change"),
    path('tags/<pk>/delete/', views.TagDeleteView.as_view(), name="tag-delete"),

]

urlpatterns += [
    path('channels/list/', views.ChannelListView.as_view(), name='channel-list'),
    path('channels/create/', views.ChannelCreateView.as_view(), name='channel-create'),
    path('channels/<pk>/', views.ChannelDetailView.as_view(), name="channel-detail"),
    path('channels/<pk>/update/', views.ChannelUpdateView.as_view(), name="channel-change"),
    path('channels/<pk>/delete/', views.ChannelDeleteView.as_view(), name="channel-delete"),
]

urlpatterns += [
    path('posts/<slug:slug>/magic/', views.magic_publishe, name='post-magic'),
    path('posts/get/file/', views.get_new_posts_of_file, name='get_new_posts_of_file'),
    path('posts/get/net/', views.get_new_posts_of_network, name='get_new_posts_of_network'),
    path('authors/<pk>/posts/list/', views.PostByAuthorListView.as_view(), name="author-post-list"),
    path('channels/<id>/posts/list/', views.PostByChannelListView.as_view(), name="channel-posts"),
    path('tags/<pk>/posts/list/', views.PostByTagListView.as_view(), name="tag-posts"),
]