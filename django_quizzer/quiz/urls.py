from django.urls import path

from django_quizzer.quiz.views import all_quizzes, search_view, start_quiz, leaderboard_view

urlpatterns = [
    path('all_quizzes/', all_quizzes, name='all_quizzes'),
    path('search/<str:category>', search_view, name='search'),
    path('<int:quiz_id>', start_quiz, name='start_quiz'),
    path('leaderboard/', leaderboard_view, name='leaderboard'),
]
