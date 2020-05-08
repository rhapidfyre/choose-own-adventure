from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
  author  = models.OneToOneField(User,on_delete=models.CASCADE)
  title   = models.CharField(max_length=128)
  created = models.DateTimeField(auto_now=False,auto_now_add=True)
  edited  = models.DateTimeField(auto_now=True)
  hidden  = models.BooleanField(default=False) #If only admins should see it 
  message = models.TextField()
  
class Comments(models.Model):
  author  = models.OneToOneField(User,on_delete=models.CASCADE)
  topic   = models.OneToOneField(Post,on_delete=models.CASCADE)
  title   = models.CharField(max_length=128)
  created = models.DateTimeField(auto_now=False,auto_now_add=True)
  edited  = models.DateTimeField(auto_now=True)
  hidden  = models.BooleanField(default=False) # AKA: Soft-Delete