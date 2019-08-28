from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Client, Answer
from django.utils import timezone
from .forms import AnswerForm

def landing_page(request):
    posts = Post.objects.filter(created_date__lte=timezone.now()).order_by('created_date')
    ip, req_time = get_client_ip(request)
    return render(request, 'blog/landing_page.html', {'ip': ip, 'req_time': req_time})

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

def answer_new(request):
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = get_client_ip(request)[0]
            answer.created_time = timezone.now()
            answer.save()
            return redirect('answer_detail', pk=answer.pk)
    else:
        form = AnswerForm()
        return render(request, 'blog/answer_new.html', {'form': form})

def answer_detail(request, pk):
    answer = get_object_or_404(Answer, pk=pk)
    id = f"Номер вашей заявки: {answer.id}"
    answer = f"Кому вы должны: {answer.step_1}; " \
               f"Сколько: {answer.step_2}; Просрочки: {answer.step_3}; " \
               f"Залог: {answer.step_4}; Имя: {answer.step_5}; Телефон: {answer.step_6}"
    return render(request, 'blog/final.html', {'id': id, 'answer': answer})

def procedury(request):
    return render(request, 'blog/procedury.html')