from django import forms
from django_quizzer.quiz.models import Quiz, Question, Category


class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'description', 'category', 'thumbnail']


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'option_1', 'option_2', 'option_3', 'option_4', 'answer']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
