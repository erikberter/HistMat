from django.shortcuts import render

from apps.Trivia.models import *
from django.shortcuts import render, get_object_or_404
from django.http import Http404, JsonResponse



from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.contrib.auth.mixins import LoginRequiredMixin

class QuizHomeView(TemplateView):
    template_name = 'Trivia/home.html'
    model = Quiz

class QuizListView(ListView):
    template_name = 'Trivia/Quiz/list.html'
    model = Quiz

    

class QuizCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'Trivia/Quiz/create.html'
    model = Quiz

    fields = [ 
        "name", 
        "description",
        "status"
        ] 

class QuizDetailView(DetailView):
    template_name = 'Trivia/Quiz/detail.html'
    model = Quiz


class QuizUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'Trivia/Quiz/update.html'
    model = Quiz
    fields = [ 
        "name", 
        "description",
        "status"
    ] 

class QuizDeleteView(LoginRequiredMixin, DeleteView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'Trivia/Quiz/confirm_delete.html'
    model = Quiz

class QuizPlayView(DetailView):
    template_name = 'Trivia/Quiz/play.html'
    model = Quiz

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