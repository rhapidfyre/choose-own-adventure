from django.shortcuts import render, redirect
from . import forms
from .forms import NewPostForm, NewReplyForm
from .models import Messages, PostTags
from django.core import exceptions
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import MessageSerializer, PostTagsSerializer


class MessageViewSet(viewsets.ModelViewSet):
  queryset = Messages.objects.all()
  serializer_class = MessageSerializer
  permission_classes = [permissions.IsAuthenticated]
  def perform_create(self, serializer):
    serializer.save(author=self.request.user)

class PostTagViewSet(viewsets.ModelViewSet):
  queryset = PostTags.objects.all()
  serializer_class = PostTagsSerializer
  permission_classes = [permissions.IsAuthenticated]

# Create your views here.
@login_required
def searchForums(request):
  page_data = {"pdata":[],"pmsg":"Ready","count":0,"showhidden":False}
  page_data["showhidden"] = request.user.is_superuser
  
  if request.method == 'GET' and 'search' in request.GET:
    try:
      page_data["pdata"] = Messages.objects.filter(tags=True).order_by("-created")
    except Messages.DoesNotExist:
      pass
    return render(request, "forums/search.html", context=page_data)
  else:
    return redirect("forums/index.html")
  
@login_required
def displayForums(request):
  if len(PostTags.objects.all()) < 4:
    PostTags.objects.get_or_create(tag="Admin Post")
    PostTags.objects.get_or_create(tag="Unrelated")
    PostTags.objects.get_or_create(tag="General")
    PostTags.objects.get_or_create(tag="Support")

  page_data = {"pdata":[],"pmsg":"Ready","count":0,"showhidden":False}
  
  entries = []
  try:
    entries = Messages.objects.filter(replyTo__isnull=True)
  except Messages.DoesNotExist:
    pass
  
  if entries.count() > 0:
    page_data = {
      "pdata":entries.order_by("-created"),
      "count":entries.count(),
      "pmsg":"Successfully retrieved posts",
      "showhidden":False
    }
    
  page_data["showhidden"] = request.user.is_superuser
  
  if request.method == 'POST' and 'new-post' in request.POST:
    postadd_form = NewPostForm(request.POST)
    if (postadd_form.is_valid()):
      titl    = postadd_form.cleaned_data["title"]
      msg     = postadd_form.cleaned_data["message"]
      taglist = postadd_form.cleaned_data["tags"]
      obj = Messages(author=request.user,title=titl,message=msg)
      obj.save()
      for k in postadd_form.cleaned_data['tags']:
        obj.tags.add(k)
  
  page_data["newpost"] = NewPostForm()
  return render(request, "forums/index.html", context=page_data)


@login_required
def displayThread(request):
  page_data = {"post": 0, "replies": [], "count": 0, "pmsg": ""}
  post_id = 0
  
  if request.method == 'POST':
    post_id = int(request.POST.get('reply-to'))
    reply_form = NewReplyForm(request.POST)
    if (reply_form.is_valid()):
      Messages(author = request.user,
        replyTo = Messages.objects.get(id = post_id),
        message = reply_form.cleaned_data["message"],
        title   = ""
      ).save()
    else:
      page_data["pmsg"] = page_data["pmsg"] + "Failed to Create Reply"
  
  elif request.method == 'GET' and 'id' in request.GET:
    post_id = int(request.GET.get('id'))
    
  else:
    return redirect("forums/index.html")
    
  page_data["post"] = post_id;
  
  try:
    page_data["opost"] = Messages.objects.get(id = post_id)
    page_data["pmsg"] = page_data["pmsg"] + "Original Post Found"
  
    try:
      page_data["replies"] = Messages.objects.filter(replyTo = post_id).order_by("created")
      page_data["count"] = Messages.objects.filter(replyTo = post_id).count()
      page_data["pmsg"] = page_data["pmsg"] + "/Responses Found"
    except Messages.DoesNotExist:
      page_data["pmsg"] = page_data["pmsg"] + "/No Replies Found"
      pass
      
  except Messages.DoesNotExist:
    page_data["pmsg"] = "Original Post not Found"
    pass
  
  page_data["newreply"] = NewReplyForm()
  
  return render(request, "forums/thread.html", context=page_data)
    
