from django import forms
from django_quizzer.quiz.models import Quiz


class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'description', 'category', 'thumbnail', 'file']
