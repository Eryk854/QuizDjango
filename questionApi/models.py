from django.db import models

# Create your models here.


class Question(models.Model):
    text = models.CharField(max_length=255)
    answerA = models.CharField(max_length=255)
    answerB = models.CharField(max_length=255)
    answerC = models.CharField(max_length=255)
    answerD = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=1)