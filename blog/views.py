from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Client, Answer, Choice, Question
from django.utils import timezone
from blog.forms import AnswerForm
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import ( 
    CreateView, UpdateView,
    ListView, DetailView
    )


class AnswerDetail(DetailView):
    model = Answer
    template_name = 'blog/answer_detail.html'


class AnswerCreate(CreateView):
    model = Answer
    fields = [
        "skolko",
        "komu",
        "prosrochky",
        "zalogi",
        "name",
        "phone"
        ]
    
    def form_valid(self, form):
        form.instance.author = get_client_ip(request=self.request)[0]
        return super().form_valid(form)


class AnswerUpdate(UpdateView):
    model = Answer
    fields = [
        "skolko",
        "komu",
        "prosrochky",
        "zalogi",
        "name",
        "phone"
        ]
    
    def form_valid(self, form):
        form.instance.author = get_client_ip(request=self.request)[0]
        return super().form_valid(form)


class AnswerListView(ListView):
    model = Answer
    context_object_name = 'answer_list'
    template_name = 'blog/answer_list.html'

    def get_queryset(self):
        """Return the last five published questions."""
        queryset = Answer.objects.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super(AnswerListView, self).get_context_data(**kwargs)
        return context


def landing_page(request):
    ip, req_time = get_client_ip(request)
    return render(
        request,
        'blog/landing_page.html',
        { 
         'ip': ip,
         'req_time': req_time,
        }
    )

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    request_time = timezone.now()
    if x_forwarded_for:
        client_ip = x_forwarded_for.split(',')[-1]
        Client.objects.create(ip=client_ip, request_time=request_time)
    else:
        client_ip = request.META.get('REMOTE_ADDR')
        Client.objects.create(ip=client_ip, request_time=request_time)
    return client_ip, request_time

def procedury(request):
    return render(request, 'blog/procedury.html')

def regulation(request):
    return render(request, 'blog/regulation.html')

def consent(request):
    return render(request, 'blog/consent.html')

def documents(request):
    return render(request, 'blog/documents.html')