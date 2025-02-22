from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.contrib import messages
from django.http import HttpResponse
from .models import Question, Choice
from django.utils import timezone


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"
    pk_url_kwarg = 'question_id'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'
    context_object_name = 'question'
    
    def get_object(self):
        # Get the question_id from URL and return the Question object
        question_id = self.kwargs.get('question_id')
        return get_object_or_404(Question, pk=question_id)

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

def add_question(request):
    if request.method == 'POST':
        question_text = request.POST.get('question_text')
        if question_text:
            question = Question.objects.create(
                question_text=question_text,
                pub_date=timezone.now()
            )
            return redirect('polls:detail', question_id=question.id)
    return render(request, 'polls/add_question.html')

def save_question(request):
    if request.method == 'POST':
        question_text = request.POST.get('question_text')
        pub_date = request.POST.get('pub_date')
        question = Question.objects.create(
            question_text=question_text,
            pub_date=timezone.now() if not pub_date else pub_date
        )
        return redirect('polls:detail', question_id=question.id)
    return redirect('polls:index')

def add_choice(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/add_choice.html', {'question': question})

def save_choice(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        choice_text = request.POST.get('choice_text')
        if choice_text:
            question.choice_set.create(choice_text=choice_text)
            return redirect('polls:detail', question_id=question_id)
    return redirect('polls:detail', question_id=question_id)

def edit_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    
    if request.method == 'POST':
        question_text = request.POST.get('question_text')
        if question_text:
            question.question_text = question_text
            question.save()
            return redirect('polls:index')
    
    return render(request, 'polls/edit_question.html', {'question': question})

def delete_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    question.delete()
    return redirect('polls:index')

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def edit_choice(request, question_id, choice_id):
    question = get_object_or_404(Question, pk=question_id)
    choice = get_object_or_404(Choice, pk=choice_id)
    return render(request, 'polls/edit_choice.html', {
        'question': question,
        'choice': choice
    })

def update_choice(request, question_id, choice_id):
    choice = get_object_or_404(Choice, pk=choice_id)
    if request.method == 'POST':
        choice_text = request.POST.get('choice_text')
        if choice_text:
            choice.choice_text = choice_text
            choice.save()
    return redirect('polls:detail', question_id=question_id)

def delete_choice(request, question_id, choice_id):
    choice = get_object_or_404(Choice, pk=choice_id)
    choice.delete()
    return redirect('polls:detail', question_id=question_id)