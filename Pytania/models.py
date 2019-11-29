from django.db import models



# Create your models here.
class Pytanie(models.Model):
    tresc = models.CharField(max_length=255)
    odpA = models.CharField(max_length=255)
    odpB = models.CharField(max_length=255)
    odpC = models.CharField(max_length=255)
    odpD = models.CharField(max_length=255)
    poprawnaOdp = models.CharField(max_length=1)