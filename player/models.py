from django.db import models
from creator.models import Slide, AdventureContainer
from django.contrib.auth.models import User


class Player(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    checkPoint = models.ForeignKey(Slide, on_delete = models.SET_NULL, null=True)
    health = models.IntegerField(default=100)
    checkPointSet = models.BooleanField(default=False)

class UserStatistics(models.Model):
    user = models.ForeignKey(User, on_delete = models.SET_NULL, null=True) #Stores first_name, last_name, username, password
    adventure = models.ForeignKey(AdventureContainer, on_delete = models.CASCADE)
    highestWinningHealth = models.IntegerField(default=0)
    timesPlayed = models.IntegerField(default=0)
    timesWon = models.IntegerField(default=0)
    timesLost = models.IntegerField(default=0)
    
# Create your models here.
