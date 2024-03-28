from django.urls import path

from django_quizzer.account.views import RegisterView, logout,edit_profile, delete_profile, LoginUserView, ProfileView

urlpatterns = [
    path('login/', LoginUserView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', logout, name='logout'),

    path('profile/<str:username>', ProfileView.as_view(), name='profile'),
    path('profile/<str:username>/edit/', edit_profile, name='edit_profile'),
    path('profile/<str:username>/delete/', delete_profile, name='delete_profile'),
]
