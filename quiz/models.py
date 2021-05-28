from django.contrib.auth.models import AbstractUser
from django.db import models

class Stud_Ans(models.Model):
    qna = models.JSONField(null=True)

class User(AbstractUser):
    is_teacher = models.BooleanField(default=False)
    recorded_Ans = models.ManyToManyField(Stud_Ans, blank=True, related_name="recorded_Ans")


class CreateQuiz(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    number_of_questions = models.IntegerField()
    category = models.CharField(max_length=64)
    difficulty = models.CharField(max_length=64)
    type_of_question = models.CharField(max_length=64)
