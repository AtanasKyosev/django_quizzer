from django.db.models import Count
from django.shortcuts import render
from django.views import generic as views
from django_quizzer.quiz.models import UserRank, Quiz


class IndexView(views.TemplateView):
    template_name = 'web/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        leaderboard_users = UserRank.objects.order_by('rank')[:3]
        context['leaderboard_users'] = leaderboard_users

        quizzes = Quiz.objects.annotate(question_count=Count('question')).filter(question_count__gte=3).order_by(
            '-created_at')[:3]
        context['quizzes'] = quizzes

        return context


class AboutView(views.TemplateView):
    template_name = 'web/about.html'


class FAQsView(views.TemplateView):
    template_name = 'web/FAQs.html'


def handler404(request, exception):
    return render(request, '404_page.html', status=404)
