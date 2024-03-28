from django.contrib.auth.models import User
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import generic as views
from django_quizzer.account.models import Profile
from django_quizzer.quiz.models import QuizSubmission


# Regiser View
class RegisterView(views.CreateView):
    model = User
    fields = ['username', 'email', 'password']
    template_name = 'account/register_user.html'

    def form_valid(self, form):
        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        password2 = self.request.POST.get('password2')

        if password != password2:
            messages.error(self.request, 'Passwords do not match.')
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(self.request, 'Email already used.')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(self.request, 'Username already taken.')
            return redirect('register')

        user = form.save()
        user.set_password(password)
        user.save()

        new_profile = Profile.objects.create(user=user)
        new_profile.save()

        user_login = authenticate(username=username, password=password)
        login(self.request, user_login)

        return redirect('profile', user.username)

    def form_invalid(self, form):
        messages.error(self.request, 'Username already taken.')
        return super().form_invalid(form)

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:

            return redirect('profile', request.user.username)
        return super().dispatch(request, *args, **kwargs)


# Login View
class LoginUserView(views.View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('profile', request.user.username)
        return render(request, 'account/login_user.html', {})

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('profile', username=user.username)
        else:
            messages.error(request, 'Credentials Invalid!')
            return redirect('login')


# Logout View
@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('index')


# Profile View
class ProfileView(views.DetailView):
    @staticmethod
    @login_required(login_url='login')
    def get(request, username):
        user_object = User.objects.get(username=username)
        user_profile = Profile.objects.get(user=user_object)
        submissions = QuizSubmission.objects.filter(user=user_object)

        context = {
            'user_profile': user_profile,
            'submissions': submissions,
        }

        return render(request, 'account/profile.html', context)


# Edit View
@login_required(login_url='login')
def edit_profile(request, username):
    user_object = User.objects.get(username=username)
    user_profile = Profile.objects.get(user=user_object)

    if request.user.profile != user_profile:
        return redirect('profile', user_object.username)

    if request.method == 'POST':
        if request.FILES.get('profile_img') is not None:
            user_profile.profile_img = request.FILES.get('profile_img')
            user_profile.save()

        if request.POST.get('email') is not None:
            u = User.objects.filter(email=request.POST.get('email')).first()

            if u is None:
                user_object.email = request.POST.get('email')
                user_object.save()
            else:
                if u != user_object:
                    messages.info(request, 'Email Already Used. Try again!')
                    return redirect('edit_profile')

        if request.POST.get('username') is not None:
            u = User.objects.filter(username=request.POST.get('username')).first()

            if u is None:
                user_object.username = request.POST.get('username')
                user_object.save()
            else:
                if u != user_object:
                    messages.info(request, 'Username Already Taken. Try again!')
                    return redirect('edit_profile')

        user_object.first_name = request.POST.get('first_name')
        user_object.last_name = request.POST.get('last_name')
        user_object.save()

        user_profile.location = request.POST.get('location')
        user_profile.gender = request.POST.get('gender')
        user_profile.bio = request.POST.get('bio')
        user_profile.save()

        return redirect('profile', user_object.username)

    context = {'user_profile': user_profile,}

    return render(request, 'account/edit_user.html', context)

# Delete View
@login_required(login_url='login')
def delete_profile(request, username):
    user_object = User.objects.get(username=username)
    user_profile = Profile.objects.get(user=user_object)

    if request.method == 'POST':
        user_profile.delete()
        user_object.delete()
        return redirect('index')

    if request.user.profile != user_profile:
        if not request.user.is_superuser:
            return redirect('profile', user_object.username)
        else:
            pass

    context = {
        'user_profile': user_profile,
    }

    return render(request, 'account/delete_user.html', context)




