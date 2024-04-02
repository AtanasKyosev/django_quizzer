from django.urls import path
from django_quizzer.administration.views import users_list, update_user_to_staff, quizzes_list, create_quiz, edit_quiz, \
    delete_quiz, administration, questions_view, add_question, edit_question, delete_question, add_category

urlpatterns = [
    path('', administration, name='administration'),
    path('users_list/', users_list, name='users_list'),
    path('update_user_to_staff/<str:username>/', update_user_to_staff, name='update_user_to_staff'),

    path('add_category/', add_category, name='add_category'),

    path('quizzes_list/', quizzes_list, name='quizzes_list'),
    path('create_quiz/', create_quiz, name='create_quiz'),
    path('edit_quiz/<int:quiz_id>/', edit_quiz, name='edit_quiz'),
    path('delete_quiz/<int:quiz_id>/', delete_quiz, name='delete_quiz'),

    path('questions/<int:quiz_id>/', questions_view, name='questions'),
    path('add_question/<int:quiz_id>/', add_question, name='add_question'),
    path('edit_question/<int:quiz_id>/<int:question_id>/', edit_question, name='edit_question'),
    path('delete_question/<int:quiz_id>/<int:question_id>/', delete_question, name='delete_question'),
]
