from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone

from .models import Question
from .models import Choice


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions
        (excluding those in the future)
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    p = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': p,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))


def create_question(request):
    if (request.POST):
        try:
            q = Question(question_text=request.POST["question_text"],
                         pub_date=timezone.now())
            q.save()
            for i in range(1, 4):
                choice_text = request.POST['choice{}'.format(i)]
                c = Choice(question=q, choice_text=choice_text)
                c.save()
        except (KeyError):
            return render(request, 'polls/index.html')

        return HttpResponseRedirect(reverse('polls:detail', args=(q.id,)))
    else:
        return render(request, 'polls/create.html')
