from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from curiosity.models import Post, Tag, Channel, PostAuthor
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import permission_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class PostListView(ListView):
    models = Post
    fields = "__all__"

    paginate_by=10


class PostCreateView(CreateView):
    models = Post
    fields = "__all__"


class PostUpdateView(UpdateView):
    models = Post
    fields = "__all__"


class PostDetailView(DetailView):
    models = Post
    query_pk_and_slug = True
    queryset = Post.objects.all()
    fields = "__all__"

    def get_queryset(self):
        return self.queryset.filter(slug=self.kwargs.get('slug'))


class PostDeleteView(DeleteView):
    model = Post
    fields = "__all__"


class PostAuthorListView(ListView):
    models = PostAuthor
    fields = "__all__"

    def get_context_data(self, **kwargs):
        context = super(PostAuthorListView, self).get_context_data(**kwargs)
        context['author'] = get_object_or_404(PostAuthor, pk=self.kwargs['pk'])
        return context
    paginate_by=10


class TagListView(ListView):
    models = Post
    fields = "__all__"

    paginate_by=10


class TagCreateView(CreateView):
    models = Post
    fields = "__all__"


class TagUpdateView(UpdateView):
    models = Post
    fields = "__all__"


class TagDetailView(DetailView):
    models = Post
    query_pk_and_slug = True
    queryset = Post.objects.all()
    fields = "__all__"

    def get_queryset(self):
        return self.queryset.filter(slug=self.kwargs.get('slug'))


class TagDeleteView(DeleteView):
    model = Post
    fields = "__all__"


class ChannelListView(ListView):
    models = Post
    fields = "__all__"

    paginate_by=10


class ChannelCreateView(CreateView):
    models = Channel
    fields = "__all__"


class ChannelUpdateView(UpdateView):
    models = Channel
    fields = "__all__"


class ChannelDetailView(DetailView):
    models = Channel
    query_pk_and_slug = True
    queryset = Channel.objects.all()
    fields = "__all__"

    def get_queryset(self):
        return self.queryset.filter(slug=self.kwargs.get('slug'))


class ChannelDeleteView(DeleteView):
    model = Channel
    fields = "__all__"


class UserListView(ListView):
    models = User
    fields = "__all__"

    paginate_by=10


class UserCreateView(CreateView):
    models = User
    fields = "__all__"


class UserUpdateView(UpdateView):
    models = User
    fields = "__all__"


class UserDetailView(DetailView):
    models = User
    query_pk_and_slug = True
    queryset = User.objects.all()
    fields = "__all__"

    def get_queryset(self):
        return self.queryset.filter(slug=self.kwargs.get('slug'))


class UserDeleteView(DeleteView):
    model = User
    fields = "__all__"


class PostAuthorCreateView(CreateView):
    models = PostAuthor
    fields = "__all__"


class PostAuthorUpdateView(UpdateView):
    models = PostAuthor
    fields = "__all__"


class PostAuthorDetailView(DetailView):
    models = PostAuthor
    queryset = PostAuthor.objects.all()
    fields = "__all__"

    def get_queryset(self):
        return self.queryset.filter(user=self.kwargs.get('user'))


class PostAuthorDeleteView(DeleteView):
    model = PostAuthor
    fields = "__all__"


class PostByChannelListView(ListView):
    model = Post


class PostByTagListView(ListView):
    model = Post


class PostByAuthorListView(LoginRequiredMixin, ListView):
    models = Post
    query_pk_and_slug = True
    queryset = Post.objects.all()
    template_name = "curiosity/pubpost_list_author_user.html"

    paginate_by=10

    def get_queryset(self):
        return self.queryset.filter(author_id=self.request.user.id)
    

def index(request):
    """Просмотр функции для главной страницы сайта."""

    # Сформировать подсчеты некоторых из основных объектов
    num_posts = Post.objects.all().count()
    num_channels = Channel.objects.all().count()

    # Опубликованные посты (status = 'a')
    num_pub = len([post.status for post in Post.objects.all() if post.status == "Опубликован"])
    num_new = len([post.status for post in Post.objects.all() if post.status == "Обнаружен"])
    # «Все ()» подразумевается по умолчанию.    
    num_tags = Tag.objects.count()

    # Количество посещений этой cnhfybws, поскольку, подсчитанных в переменной сеанса.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1

    context = {
        'num_new': num_new,
        'num_posts': num_posts,
        'num_channels': num_channels,
        'num_pub': num_pub,
        'num_tags': num_tags,
        'num_visits': num_visits,
    }

    # Рендер шаблон HTML index.html с данными в переменном контексте
    return render(request, 'curiosity/index.html', context=context)


def magic_publishe(self, request):
    context = { "user" : request.user }
    self.publish_post(self, request)
    return HttpResponseRedirect('/curiosity/', context=context)

def get_new_posts_of_file(request):
    context = { "user" : request.user }
    Post.get_new_posts_of_file()
    return HttpResponseRedirect('/curiosity/', context=context)

def get_new_posts_of_network(request):
    Post.get_new_posts_of_network()
    return HttpResponseRedirect('/curiosity/')

def trash():
    
    HOW_POST_TO_PRINT = 5
    VK_TOKEN = models.CharField(max_length=500, null=True, default="9bfae56722ff872d603c6b0aa10c9c47f42fa00de836de4e47217e44c7f06259767efb6ee95c494303a8e")
    PATH_TO_LOG = models.CharField(max_length=500, null=True, default=os.path.dirname(os.path.abspath(__file__)) + "worker/curiosity-to-vk.log")
    PATH_MY_HREF = models.CharField(max_length=500, null=True, default=os.path.dirname(os.path.abspath(__file__)) + "worker/my_href.db")
    PATH_TO_BACKUP_HREF = models.CharField(max_length=500, null=True, default=os.path.dirname(os.path.abspath(__file__)) + "worker/my_href_backup.db")
    PATH_TO_IMG_RESIZE = models.CharField(max_length=500, null=True, default=os.path.dirname(os.path.abspath(__file__)) + "worker/topics/IMG_RESIZE.png")
    PATH_TO_IMG_ORIGINAL = models.CharField(max_length=500, null=True, default=os.path.dirname(os.path.abspath(__file__)) + "worker/topics/IMG_ORIGINAL.png")
    # PATH_TO_IMG_1_COMPOSITE = models.CharField(max_length=500, null=True, default=os.path.dirname(os.path.abspath(__file__)) + "worker/topics/IMG_COMPOSITE.png")
    PATH_TO_IMG_LOGO_PAINTER = models.CharField(max_length=500, null=True, default=os.path.dirname(os.path.abspath(__file__)) + "worker/desing/logo-painter.png")
    PATH_TO_FONTS = models.CharField(max_length=500, null=True, default=os.path.dirname(os.path.abspath(__file__)) + "worker/topics/Roboto-Fonts/Roboto-Bold.ttf")
    PATH_TO_IMG_BUTTON = models.CharField(max_length=500, null=True, default=os.path.dirname(os.path.abspath(__file__)) + "worker/Button.png")
    VK_GROUP_ID = models.CharField(max_length=500, null=True, default=181925964)
    UUID4_HEX_REGEX = models.CharField(max_length=500, null=True, default=re.compile('[0-9a-f]{12}4[0-9a-f]{3}[89ab][0-9a-f]{15}\Z', re.I))
    return