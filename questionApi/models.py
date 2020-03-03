from django.db import models
from user.models import Player
# Create your models here.


class Question(models.Model):
    text = models.CharField(max_length=255)
    answerA = models.CharField(max_length=255)
    answerB = models.CharField(max_length=255)
    answerC = models.CharField(max_length=255)
    answerD = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=1)


class SuggestQuestion(models.Model):
    ANSWERS = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D')
    ]
    STATUS = [
        ('Added', 'Added'),
        ('Deleted', 'Deleted'),
        ('Wait', 'Wait for reaction')
    ]

    player = models.ForeignKey(Player, on_delete=models.PROTECT)
    text = models.CharField(max_length=255)
    answerA = models.CharField(max_length=255)
    answerB = models.CharField(max_length=255)
    answerC = models.CharField(max_length=255)
    answerD = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=1, choices=ANSWERS)
    status = models.CharField(max_length=10, choices=STATUS, default='Wait')
