from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django_quizzer.account.models import Profile
from django_quizzer.quiz.forms import QuizForm, QuestionForm, CategoryForm
from django_quizzer.quiz.models import Category, Quiz, Question


@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def administration(request):
    return render(request, 'administration/administration.html', context={})


@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def users_list(request):
    users = User.objects.all().order_by('-date_joined')

    context = {
        'users': users,
    }

    return render(request, 'administration/user_partials/users_list.html', context)


@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def update_user_to_staff(request, username):
    user = get_object_or_404(User, username=username)

    if request.method == 'POST':

        if 'is_staff' in request.POST:
            is_staff = request.POST.get('is_staff') == 'on'
            user.is_staff = is_staff
            user.save()

        else:
            user.is_staff = False
            user.save()

        return redirect('users_list')

    return redirect('users_list')


@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def quizzes_list(request):
    quizzes = Quiz.objects.all().order_by('-created_at')
    categories = Category.objects.all().order_by('name')

    context = {
        'quizzes': quizzes,
        'categories': categories,
    }

    return render(request, 'administration/quiz_partials/quizzes_list.html', context)


@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('quizzes_list')
    else:
        form = CategoryForm()

    context = {
        'form': form,
    }

    return render(request, 'administration/category_partials/add_category.html', context)


@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def create_quiz(request):
    user_object = User.objects.get(username=request.user)
    user_profile = Profile.objects.get(user=user_object)
    categories = Category.objects.all().order_by('name')

    if request.method == 'POST':
        form = QuizForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('quizzes_list')
    else:
        form = QuizForm()

    context = {
        'form': form,
        'user_profile': user_profile,
        'categories': categories,
    }

    return render(request, 'administration/quiz_partials/create_quiz.html', context)


@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def edit_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    categories = Category.objects.all().order_by('name')

    if request.method == 'POST':
        form = QuizForm(request.POST, request.FILES, instance=quiz)
        if form.is_valid():
            form.save()
            return redirect('quizzes_list')
    else:
        form = QuizForm(instance=quiz)

    context = {
        'form': form,
        'quiz': quiz,
        'categories': categories,
    }

    return render(request, 'administration/quiz_partials/edit_quiz.html', context)


@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def delete_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)

    if request.method == 'POST':
        quiz.delete()
        return redirect('quizzes_list')

    context = {
        'quiz': quiz,
    }

    return render(request, 'administration/quiz_partials/delete_quiz.html', context)


@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def questions_view(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    questions = Question.objects.filter(quiz=quiz).all()
    total_questions = questions.count()

    context = {
        'quiz': quiz,
        'questions': questions,
        'total_questions': total_questions,
    }

    return render(request, 'administration/question_partials/questions.html', context)


@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def add_question(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.quiz = quiz
            question.save()
            return redirect('questions', quiz.id)
    else:
        form = QuestionForm()

    context = {
        'quiz': quiz,
        'form': form,
    }

    return render(request, 'administration/question_partials/add_question.html', context)


@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def edit_question(request, quiz_id, question_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    question = get_object_or_404(Question, pk=question_id)

    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect('questions', quiz_id=quiz.id)
    else:
        form = QuestionForm(instance=question)

    context = {
        'quiz': quiz,
        'form': form,
        'question': question,
    }

    return render(request, 'administration/question_partials/edit_question.html', context)


@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def delete_question(request, quiz_id, question_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    question = get_object_or_404(Question, pk=question_id)

    if request.method == 'POST':
        question.delete()
        return redirect('questions', quiz_id=quiz.id)

