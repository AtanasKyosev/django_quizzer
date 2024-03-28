from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django_quizzer import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('django_quizzer.web.urls')),
    path('user/', include('django_quizzer.account.urls')),
    path('quiz/', include('django_quizzer.quiz.urls')),
    path('administration/', include('django_quizzer.administration.urls'))
]

handler404 = 'django_quizzer.web.views.handler404'

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


