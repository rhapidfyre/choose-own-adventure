from django.db import models
from creator.models import Slide
from django.contrib.auth.models import User


class Player(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    checkPoint = models.ForeignKey(Slide, on_delete = models.SET_NULL, null=True)
    health = models.IntegerField(default=100)
    checkPointSet = models.BooleanField(default=False)
    
    
# Create your models here.
