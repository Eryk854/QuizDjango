from django.db import models

# Create your models here.
class Player(models.Model):
    email = models.EmailField(max_length=254,blank=False)
    best_score = models.IntegerField(default=-1)