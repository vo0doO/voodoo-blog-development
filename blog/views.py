from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Client, Answer, Question, Choice
from django.utils import timezone
from django.urls import reverse
from .forms import AnswerForm

def landing_page(request):
    ip, req_time = get_client_ip(request)
    return render(request, 'blog/landing_page.html', {'ip': ip, 'req_time': req_time})


def answer_new(request):
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = get_client_ip(request)[0]
            answer.created_time = timezone.now()
            answer.save()
            return redirect('final', pk=answer.id)
    else:
        form = AnswerForm()
        return render(request, 'blog/answer_new.html', {'form': form })


def final(request, pk):
    answer = get_object_or_404(Answer, pk=pk)
    id = f"Номер вашей заявки: {answer.id}"
    return render(request, 'blog/final.html', {'id': id, 'answer': answer})


def questions_latest(request):
    latest_question_list = Question.objects.all()[:]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'blog/latest.html', context)


def detail(request, question_id):
    step_max = str(len(Question.objects.all()))
    step_current = str((question_id))
    step_view_html = f"Шаг {step_current}/{step_max}"
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'blog/detail.html', {'question': question, 'step_view_html': step_view_html})


def results(request, question_id):
    response = "Ты видишь результаты вопроса"
    return HttpResponse(f"{response}: {question_id}")


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    step_max = str(len(Question.objects.all()))
    step_current = str((question_id))
    step_view_html = f"Шаг {step_current}/{step_max}"
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'][0])
        print(selected_choice)
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'blog/detail.html', {
            'question': question,
            'step_view_html': step_view_html,
            'error_message': "Вы не выбрали выбор."
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Всегда возвращайте HttpResponseRedirect после успешного обращения с
        # данными POST. Это предотвращает публикацию данных дважды, если пользователь
        # нажимает кнопку Назад.
        return HttpResponseRedirect(reverse('blog:results', args=(question.id,)))


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