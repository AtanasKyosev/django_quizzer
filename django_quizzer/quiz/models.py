from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from django.db import models
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


class Question(models.Model):
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
    )
    question_text = models.CharField(
        max_length=255
    )
    option_1 = models.CharField(
        max_length=255
    )
    option_2 = models.CharField(
        max_length=255
    )
    option_3 = models.CharField(
        max_length=255)
    option_4 = models.CharField(
        max_length=255
    )
    answer = models.CharField(
        max_length=255
    )

    def __str__(self):
        return self.question_text


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
        auto_now=True,
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
