from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    GENDER = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )

    bio = models.TextField(
        max_length=500,
        blank=True,
        null=True,
    )

    profile_img = models.ImageField(
        upload_to='profile_images',
        null=True,
        blank=True,
        verbose_name="Profile Picture",
    )

    location = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )

    gender = models.CharField(
        max_length=50,
        choices=GENDER,
        blank=True,
        null=True,
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='User Object'
    )

    def __str__(self):
        return self.user.username

    @property
    def full_name(self):
        if self.user.first_name and self.user.last_name:
            return f"{self.user.first_name} {self.user.last_name}"
        return self.user.first_name or self.user.last_name

