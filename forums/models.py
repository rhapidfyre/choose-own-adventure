from django.db import models
from django.contrib.auth.models import User

#class Post(models.Model):
#  author  = models.ForeignKey(User,on_delete=models.CASCADE)
#  title   = models.CharField(max_length=128)
#  created = models.DateTimeField(auto_now=False,auto_now_add=True)
#  edited  = models.DateTimeField(auto_now=True)
#  hidden  = models.BooleanField(default=False) #If only admins should see it 
#  message = models.TextField()
#  
#class Comments(models.Model):
#  author  = models.ForeignKey(User, on_delete=models.CASCADE)
#  topic   = models.ForeignKey(Post, on_delete=models.CASCADE)
#  title   = models.CharField(max_length=128)
#  created = models.DateTimeField(auto_now=False,auto_now_add=True)
#  edited  = models.DateTimeField(auto_now=True)
#  hidden  = models.BooleanField(default=False) # AKA: Soft-Delete
#  message = models.TextField()
  
# Since they're identical, we'll just use one model
class Messages(models.Model):
  TAG_CHOICES  = (
    ('unrelated', 'Unrelated'),
    ('admin', 'Admin Post'),
    ('creator', 'Creator'),
    ('stats', 'Stats'),
    ('general', 'General')
  )
  author   = models.ForeignKey(User, on_delete=models.CASCADE)
  replyTo  = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
  title    = models.CharField(max_length=128)
  created  = models.DateTimeField(auto_now=False,auto_now_add=True)
  edited   = models.DateTimeField(auto_now=True)
  hidden   = models.BooleanField(default=False) # AKA: Soft-Delete
  message  = models.TextField()
  category = models.CharField(max_length = 96, choices = TAG_CHOICES, default = 'unrelated')
  
