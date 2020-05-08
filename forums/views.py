from django.shortcuts import render, redirect
from . import forms
from . import models
from django.core import exceptions
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def displayForums(request):
  return render(request, "login/", context="")