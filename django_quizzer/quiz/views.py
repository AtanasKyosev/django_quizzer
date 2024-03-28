from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django_quizzer.account.models import Profile
from django_quizzer.quiz.models import Category, Quiz, QuizSubmission, UserRank


def all_quizzes(request):
    quizzes = Quiz.objects.all().order_by('-created_at')
    categories = Category.objects.all().order_by('name')

    context = {
        'quizzes': quizzes,
        'categories': categories,
    }

    return render(request, 'quiz/all_quizzes.html', context)


def search_view(request, category):
    if request.GET.get('search_pattern') is not None:
        search_pattern = request.GET.get('search_pattern')
        quizzes = Quiz.objects.filter(title__icontains=search_pattern)

    elif category != " ":
        quizzes = Quiz.objects.filter(category__name=category)

    else:
        quizzes = Quiz.objects.all().order_by('-created_at')

    categories = Category.objects.all().order_by('name')

    context = {
        'quizzes': quizzes,
        'categories': categories,
    }

    return render(request, 'quiz/all_quizzes.html', context)


@login_required(login_url='login')
def quiz_view(request, quiz_id):
    user_object = User.objects.get(username=request.user)
    user_profile = Profile.objects.get(user=user_object)
    quiz = Quiz.objects.filter(id=quiz_id).first()
    total_questions = quiz.question_set.all().count()

    if request.method == 'POST':
        score = int(request.POST.get('score', 0))

        existing_submission = QuizSubmission.objects.filter(user=request.user, quiz=quiz).first()

        if existing_submission:

            messages.success(request, f'This time you got {score} out of {total_questions}!')
            existing_submission.score = score
            existing_submission.save()

            return redirect('quiz', quiz_id)

        submission = QuizSubmission(user=request.user, quiz=quiz, score=score)
        submission.save()

        messages.success(request, f'Quiz Submitted Successfully You got {score} out of {total_questions}!')

        return redirect('quiz', quiz_id)

    if quiz is not None:

        context = {
            'quiz': quiz,
            'user_profile': user_profile,
        }

    else:

        return redirect('quiz_catalogue')

    return render(request, 'quiz/quiz.html', context)


def leaderboard_view(request):
    leaderboard_users = UserRank.objects.order_by('rank')[:100]

    context = {
        'leaderboard_users': leaderboard_users,
    }

    return render(request, 'quiz/leaderboard.html', context)
