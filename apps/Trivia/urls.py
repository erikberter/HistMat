from django.urls import path
from . import views
from django.conf import settings

app_name = 'trivia'

urlpatterns = [
    path("quiz_list/", views.quiz_list, name='quiz_list'),
    path("quiz/<int:quiz_pk>/", views.quiz_detail, name='quiz_detail'),
    path("quiz/<int:quiz_pk>/questions/", views.quiz, name='quiz'),
    path("quiz/question/", views.question, name='question_detail')
]