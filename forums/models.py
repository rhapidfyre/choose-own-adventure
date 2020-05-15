from django.db import models
from django.contrib.auth.models import User

class PostTags(models.Model):
  tag = models.CharField(max_length = 32)
  def __str__(self):
    return self.tag
  def split_tags(self):
    return self.tags.split(',')
  
class Messages(models.Model):
  author   = models.ForeignKey(User, on_delete=models.CASCADE)
  replyTo  = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
  title    = models.CharField(max_length=42)
  created  = models.DateTimeField(auto_now=False,auto_now_add=True)
  edited   = models.DateTimeField(auto_now=True)
  hidden   = models.BooleanField(default=False) # AKA: Soft-Delete
  message  = models.TextField()
  tags     = models.ManyToManyField(PostTags)
  
