from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Client, Answer, Choice, Question
from django.utils import timezone
from blog.forms import AnswerForm
from django.http import HttpResponseRedirect
from django.views.generic import( 
    CreateView, UpdateView,
    ListView, DetailView
    )


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


class AnswerResult(DetailView):
    model = Answer
    template_name = 'blog/answer_result.html'


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


def answer_new(request):
    ip, req_time = get_client_ip(request)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save()
            answer.author = ip
            answer.created_time = req_time
            answer.save()
            return redirect(request, 'blog:final', pk=answer.pk)

    else:
        form = AnswerForm()

    return render(request, 'blog/answer_new.html', {"form": form})


def final(request, pk):
    answer = get_object_or_404(Answer, pk=pk)
    id = f"Номер вашей заявки: {answer.id}"
    return render(request, 'blog/final.html', {'id': id})


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


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'blog/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('blog:results', args=(question.id,)))