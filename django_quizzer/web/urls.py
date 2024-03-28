from django.urls import path
from django_quizzer.web.views import IndexView, AboutView, FAQsView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('faqs/', FAQsView.as_view(), name='FAQs'),
    path('about/', AboutView.as_view(), name='about'),
]
