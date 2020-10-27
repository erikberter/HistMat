from django.urls import path
from . import views
from django.conf import settings

app_name = 'trivia'

urlpatterns = [
    path("quiz_list/", views.QuizListView.as_view(), name='quiz_list'),
    path("quiz/<int:pk>/", views.QuizDetailView.as_view(), name='quiz_detail'),
    path("quiz/<int:pk>/questions/", views.QuizView.as_view(), name='quiz'),
    path("quiz/<int:quiz_pk>/question/<int:question_number>/", views.question, name='question_detail'),
    path("quiz/<int:quiz_pk>/question/<int:question_number>/answer/", views.question_check, name='question_answer'),
]