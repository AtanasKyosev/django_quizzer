from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render, redirect
from django_quizzer.quiz.models import Category, Quiz, QuizSubmission, UserRank, Question


def all_quizzes(request):
    quizzes = Quiz.objects.all().order_by('-created_at')
    categories = Category.objects.all().order_by('name')

    for quiz in quizzes:
        if quiz.question_set.count() < 3:
            quizzes = quizzes.exclude(id=quiz.id)

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

    # Exclude quizzes with less than 3 questions
    quizzes = quizzes.annotate(question_count=Count('question')).filter(question_count__gte=3)

    categories = Category.objects.all().order_by('name')

    context = {
        'quizzes': quizzes,
        'categories': categories,
    }

    return render(request, 'quiz/all_quizzes.html', context)


@login_required(login_url='login')
def start_quiz(request, quiz_id):
    quiz = Quiz.objects.filter(id=quiz_id).first()
    user = request.user
    questions = Question.objects.filter(quiz=quiz).all()
    total_questions = questions.count()

    if quiz is None:
        return redirect('all_quizzes')

    if request.method == 'POST':
        total = 0
        score = 0

        for question in questions:
            total += 1
            selected_option = request.POST.get(f'question_{question.id}', '')

            if selected_option == '':
                continue
            if selected_option == question.answer:
                score += 1

        existing_submission = QuizSubmission.objects.filter(user=user, quiz=quiz).first()

        if existing_submission:
            existing_submission.delete()
            submission = QuizSubmission.objects.create(user=user, quiz=quiz, score=score)
            submission.save()
        else:
            submission = QuizSubmission(user=user, quiz=quiz, score=score)
            submission.save()

        context = {
            'score': score,
            'time': request.POST.get('timer'),
            'total': total,
        }

        return render(request, 'quiz/result.html', context)

    context = {
        'quiz': quiz,
        'questions': questions,
        'total_questions': total_questions,
    }

    return render(request, 'quiz/quiz.html', context)


def leaderboard_view(request):
    leaderboard_users = UserRank.objects.order_by('rank')

    context = {
        'leaderboard_users': leaderboard_users,
    }

    return render(request, 'quiz/leaderboard.html', context)
