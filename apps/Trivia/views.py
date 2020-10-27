from django.shortcuts import render

from apps.Trivia.models import *
from django.shortcuts import render, get_object_or_404
from django.http import Http404, JsonResponse

from django.views.generic import DetailView, ListView

class QuizListView(ListView):
    context_object_name = 'quiz_list'
    template_name = 'Trivia/quiz_list.html'

    def get_queryset(self):
        return Quiz.objects.filter(status='publish')


class QuizDetailView(DetailView):
    context_object_name = 'quiz'
    template_name = 'Trivia/quiz_detail.html'

    def get_queryset(self):
        return Quiz.objects.filter(status='publish')

class QuizView(DetailView):
    context_object_name = 'quiz'
    template_name = 'Trivia/quiz.html'

    def get_queryset(self):
        return Quiz.objects.filter(status='publish')


def question(request, quiz_pk, question_number):
    context = {}
    if request.is_ajax():
        context['quiz'] =  Quiz.objects.get(pk=quiz_pk)
        try:
            context['question'] = Question.objects.filter(quiz=quiz_pk)[question_number]
        except:
            raise Http404
        
        if isinstance(context['question'].cast(), MultiChoiceQuestion):
            context['answers'] = MultiChoiceAnswer.objects.filter(question=context['question'])
        
        return render(request, 'Trivia/_question.html', context)
        
    raise Http404

def question_check(request, quiz_pk, question_number):
    context = {}
    if request.is_ajax():
        question = Question.objects.filter(quiz=quiz_pk)[question_number]

        if 'answer' not in request.POST:
            raise Http404

        data = {}
        data['answer'] = request.POST.get('answer')
        if isinstance(question.cast(), MultiChoiceQuestion):
            data['answer'] = int(data['answer'])
            print("RESP:"+str(int(data['answer'])))
        data['result'] = question.cast().is_answer_correct(data)
        return JsonResponse(data)
    raise Http404