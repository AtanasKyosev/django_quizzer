from django.contrib.auth.models import User
from django.db import models
import pandas as pd
from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver


class Category(models.Model):
    MAX_NAME_LENGTH = 50
    name = models.CharField(
        max_length=MAX_NAME_LENGTH,
    )

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Quiz(models.Model):
    MAX_TITLE_LENGHT = 100
    title = models.CharField(
        max_length=MAX_TITLE_LENGHT,
    )

    description = models.TextField()

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
    )

    file = models.FileField(
        upload_to='quiz/',
    )

    thumbnail = models.URLField(
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        verbose_name_plural = 'Quizzes'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.file:
            self.import_quiz_from_excel()

    def import_quiz_from_excel(self):
        df = pd.read_excel(self.file.path)

        for index, row in df.iterrows():
            question_text = row['Question']
            choice1 = row['A']
            choice2 = row['B']
            choice3 = row['C']
            choice4 = row['D']
            correct_answear = row['Answer']

            question = Question.objects.get_or_create(quiz=self, text=question_text)

            choice_1 = Choice.objects.get_or_create(question=question[0], text=choice1, is_correct=correct_answear == 'A')
            choice_2 = Choice.objects.get_or_create(question=question[0], text=choice2, is_correct=correct_answear == 'B')
            choice_3 = Choice.objects.get_or_create(question=question[0], text=choice3, is_correct=correct_answear == 'C')
            choice_4 = Choice.objects.get_or_create(question=question[0], text=choice4, is_correct=correct_answear == 'D')


class Question(models.Model):
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
    )

    text = models.TextField()

    def __str__(self):
        return self.text[:50]


class Choice(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE
    )

    text = models.CharField(max_length=255)

    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.question.text[:50]}, {self.text[:20]}'


class QuizSubmission(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
    )

    score = models.IntegerField()

    submited_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return f'{self.user}, {self.quiz.title}'


class UserRank(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    rank = models.IntegerField(
        blank=True,
        null=True,
    )

    total_score = models.IntegerField(
        blank=True,
        null=True,
    )

    def __str__(self):
        return f'{self.rank}, {self.user.username}'


@receiver(post_save, sender=QuizSubmission)
def update_leaderboard(sender, instance, created, **kwargs):
    if created:
        update_leaderboard()


def update_leaderboard():
    user_scores = (QuizSubmission.objects.values('user').annotate(total_score=Sum('score')).order_by('-total_score'))

    rank = 1
    for entry in user_scores:
        user_id = entry['user']
        total_score = entry['total_score']

        user_rank, created = UserRank.objects.get_or_create(user_id=user_id)
        user_rank.rank = rank
        user_rank.total_score = total_score
        user_rank.save()

        rank += 1
