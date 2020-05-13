from django.shortcuts import render, redirect
from . import forms
from . import models
from .models import Messages
from django.core import exceptions
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import MessageSerializer


class MessageViewSet(viewsets.ModelViewSet):
  queryset = Messages.objects.all()
  serializer_class = MessageSerializer
  permission_classes = [permissions.IsAuthenticated]
  def perform_create(self, serializer):
    serializer.save(author=self.request.user)


# Create your views here.
@login_required
def displayForums(request):
  page_data = {"pdata":[],"pmsg":"Ready","count":0}
  
  try:
    page_data = {
      "pdata":Messages.objects.all(),
      "count":Messages.objects.filter(username='myname', status=0).count(),
      "pmsg":"Successfully retrieved posts"
    }
  except:
    page_data = {
      "pdata":[],
      "pmsg":"There are no posts, why don't you start one?",
      "count":0
    }
  
  return render(request, "forums/index.html", context=page_data)
