from django.urls import path
from . import views
from django.conf import settings

app_name = 'trivia'

# TODO Add more secure URL pattern system

urlpatterns = [
    path("home/", views.QuizHomeView.as_view(), name='quiz_home'),
    path("quiz/list/", views.QuizListView.as_view(), name='quiz_list'),
    path("quiz/create/", views.QuizCreateView.as_view(), name='quiz_create'),
    path("quiz/<slug:slug>/detail/", views.QuizDetailView.as_view(), name='quiz_detail'),
    path("quiz/<slug:slug>/update/", views.QuizUpdateView.as_view(), name='quiz_update'),
    path("quiz/<slug:slug>/confirm_delete/", views.QuizDeleteView.as_view(), name='quiz_delete'),
    path("quiz/<slug:slug>/play/", views.QuizPlayView.as_view(), name='quiz_play'),
]