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
  return render(request, "forums/index.html", context={})
