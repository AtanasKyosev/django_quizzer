from django.contrib import admin
from django_quizzer.account.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass
