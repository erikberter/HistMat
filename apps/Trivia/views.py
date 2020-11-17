from django.shortcuts import render

from apps.Trivia.models import *
from django.shortcuts import render, get_object_or_404
from django.http import Http404, JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy


from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.contrib.auth.mixins import LoginRequiredMixin

from django.core import serializers


class QuizHomeView(TemplateView):
    template_name = 'Trivia/home.html'
    model = Quiz

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            data['my_quiz'] = Quiz.objects.filter(creator=self.request.user)
        data['popular_quiz'] = Quiz.objects.filter(status='publish').all()
        return data

class QuizListView(ListView):
    template_name = 'Trivia/Quiz/list.html'
    model = Quiz

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['quizzes'] = Quiz.objects.filter(status='publish').all()
        return context

class QuizCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'Trivia/Quiz/create.html'
    model = Quiz

    success_url = reverse_lazy('trivia:quiz_list')

    fields = ["name", "description","status"] 

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.creator = self.request.user
        obj.save()        
        return HttpResponseRedirect(self.success_url)

class QuizDetailView(DetailView):
    template_name = 'Trivia/Quiz/detail.html'
    model = Quiz
    context_object_name = "quiz"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        quiz = self.get_object()
        context['is_own_quiz'] = (quiz.creator == self.request.user)
        return context

class QuizUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'Trivia/Quiz/update.html'
    object_context_name = "quiz_object"
    model = Quiz

    fields = [ 
        "name", 
        "description",
        "status"
    ] 

class QuizDeleteView(LoginRequiredMixin, DeleteView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    success_url = reverse_lazy('trivia:quiz_list')
    template_name = 'Trivia/Quiz/confirm_delete.html'
    model = Quiz

import json
from django.core.serializers import serialize


class QuizPlayView(DetailView):
    template_name = 'Trivia/Quiz/play.html'
    model = Quiz

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            quiz = self.get_object()
            question_dict = {}
            questions_query = Question.objects.filter(quiz=quiz).all()
            question_dict = questionSelect(questions_query)
            question_dict['quiz_name'] = quiz.name
        
            return JsonResponse(question_dict)
        else:
            return super().get(self, request, *args, **kwargs)

"""def question_check(request, quiz_pk, question_number):
    context = {}
    if request.is_ajax():
        question = Question.objects.filter(quiz=quiz_pk)[question_number]

        if 'answer' not in request.POST:
            raise Http404

        data = {}
        data['answer'] = request.POST.get('answer')
        if isinstance(question.cast(), MultiChoiceQuestion):
            data['answer'] = int(data['answer'])
            
        data['result'] = question.cast().is_answer_correct(data)
        return JsonResponse(data)
    raise Http404"""