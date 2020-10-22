from django.shortcuts import render

from apps.Trivia.models import *
from django.shortcuts import render, get_object_or_404
from django.http import Http404

def quiz_list(request):
    context = {}
    context['quiz_list'] = Quiz.objects.filter(status="publish")
    return render(request, 'Trivia/quiz_list.html', context)

def quiz_detail(request, quiz_pk):
    context = {}
    context['quiz'] = get_object_or_404(Quiz, pk=quiz_pk, status='publish')
    return render(request, 'Trivia/quiz_detail.html', context)

def quiz(request, quiz_pk):
    context = {}
    context['quiz'] = get_object_or_404(Quiz, pk = quiz_pk, status='publish')
    return render(request, 'Trivia/quiz.html', context)

def question(request):
    context = {}
    if request.is_ajax():
        if 'question_number' not in request.POST or 'quiz_pk' not in request.POST:
            raise Http404
        try:
            question_number = int(request.POST.get('question_number'))
            context['question'] = Question.objects.filter(quiz=request.POST.get('quiz_pk'))[question_number]
            
            
            if isinstance(context['question'].cast(), MultiChoiceQuestion):
                context['answers'] = MultiChoiceAnswer.objects.filter(question=context['question'])
            
            return render(request, 'Trivia/_question.html', context)
        except Exception as e:
            print(e)
            raise Http404
    raise Http404