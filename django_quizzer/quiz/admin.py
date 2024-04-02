from django.contrib import admin

from django_quizzer.quiz.models import Quiz, Category, Question, QuizSubmission, UserRank


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    pass


@admin.register(QuizSubmission)
class QuizSubmissionAdmin(admin.ModelAdmin):
    pass


@admin.register(UserRank)
class UserRankAdmin(admin.ModelAdmin):
    pass
