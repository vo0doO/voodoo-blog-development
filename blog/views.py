from django.shortcuts import render, get_object_or_404, redirect
from .models import Client, Answer
from django.utils import timezone
from .forms import AnswerForm

def landing_page(request):
    ip, req_time = get_client_ip(request)
    return render(request, 'blog/landing_page.html', {'ip': ip, 'req_time': req_time})


def answer_new(request):
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save()
            answer.author = get_client_ip(request)[0]
            answer.save()
            return redirect('blog:final', pk=answer.id)
    else:
        form = AnswerForm()
    return render(request, 'blog/answer_new.html', {'form': form })


def final(request, pk):
    answer = get_object_or_404(Answer, pk=pk)
    id = f"Номер вашей заявки: {answer.pk}"
    return render(request, 'blog/final.html', {'id': id, 'pk': pk})


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    request_time = timezone.now()
    if x_forwarded_for:
        client_ip=x_forwarded_for.split(',')[-1]
        Client.objects.create(ip=client_ip, request_time=request_time)
    else:
        client_ip = request.META.get('REMOTE_ADDR')
        Client.objects.create(ip=client_ip, request_time=request_time)
    return client_ip, request_time