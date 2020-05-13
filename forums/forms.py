from django import forms
from django.forms import ModelForm
from django.core import validators
from . import models
from .models import PostTags
  
# Dynamic Form Fields
# https://stackoverflow.com/questions/22255759/django-forms-dynamic-choices-for-choicefield
class NewPostForm(forms.Form):
  def __init__(self, *args, **kwargs):
    super(NewPostForm, self).__init__(*args, **kwargs)
    self.fields['tags'] = forms.ModelMultipleChoiceField(
        queryset=PostTags.objects.all()
    )
  title = forms.CharField(max_length = 42,
    widget = forms.TextInput(attrs = {'placeholder':'My new task'}),
    validators=[validators.MaxLengthValidator(42)])
  message = forms.CharField(widget=forms.Textarea())
  tags = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=())
  
class NewReplyForm(forms.Form):
  message = forms.CharField(widget=forms.Textarea())