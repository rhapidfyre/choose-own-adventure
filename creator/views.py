from django.shortcuts import render, redirect
from . import forms
from . import models
from django.core import exceptions
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from rest_framework import permissions
from creator.serializers import UserSerializer
from creator.serializers import AdventureSerializer
from creator.serializers import SlideSerializer
from creator.serializers import GoBackSerializer
from creator.serializers import ChoiceContainerSerializer
from creator.serializers import ChoiceSerializer
from creator.serializers import NextSlideSerializer
from creator.models import AdventureContainer
from creator.models import Slide
from creator.models import GoBack
from creator.models import ChoiceContainer
from creator.models import Choice
from creator.models import NextSlide
from creator.forms import newAdventureForm
from creator.forms import editAdventureForm
from creator.forms import newSlideForm
from creator.forms import editSlideForm
from creator.forms import newChoiceForm
from creator.forms import editChoiceForm
from creator.forms import editNextSlide
from creator.forms import newNextSlide
from creator.forms import linkSlide


class AdventureViewSet(viewsets.ModelViewSet):
  queryset = AdventureContainer.objects.all()
  serializer_class = AdventureSerializer
  permission_classes = [permissions.IsAuthenticated]
  def perform_create(self, serializer):
    serializer.save(user=self.request.user)

class SlideViewSet(viewsets.ModelViewSet):
  queryset = Slide.objects.all()
  serializer_class = SlideSerializer
  permission_classes = [permissions.IsAuthenticated]

class GoBackViewSet(viewsets.ModelViewSet):
  queryset = GoBack.objects.all()
  serializer_class = GoBackSerializer
  permission_classes = [permissions.IsAuthenticated]

class ChoiceContainerViewSet(viewsets.ModelViewSet):
  queryset = ChoiceContainer.objects.all()
  serializer_class = ChoiceContainerSerializer
  permission_classes = [permissions.IsAuthenticated]

class ChoiceViewSet(viewsets.ModelViewSet):
  queryset = Choice.objects.all()
  serializer_class = ChoiceSerializer
  permission_classes = [permissions.IsAuthenticated]

class NextSlideViewSet(viewsets.ModelViewSet):
  queryset = NextSlide.objects.all()
  serializer_class = NextSlideSerializer
  permission_classes = [permissions.IsAuthenticated]
    
# Create your views here.
#/create/adv/<adventureID>/edit/<container>/edit/<choice>/assign
#/create/adv/<adventureID>/add/<container>/add</choice>/assign

#/create/adv/ - displayNewAdventure
#/create/adv/<adventureID>/add/ - displayNewSlide
#/create/adv/<adventureID>/add/<container>/add/<choice>/assign - displayNewSlide - Assign - old ContainerID and old Choice ID leading to New Slide. - Next Slide is configured from newly created slide and Choice ID
#/create/adv/<adventureID>/add/<container>/add/- displayNewChoiceForm linking to container it'll be displayed on.

#/create/adv/<adventureID>/edit/ - Edit Adventure Title
#/create/adv/<adventureID>/edit/<container>/edit - displayEditSlide - A newly created container displaying the newly created slide.
#/create/adv/<adventureID>/edit/<container>/edit/<choices> - displayEditChoice - The container and choiceID you want to edit
#/create/adv/<adventureID>/edit/<container>/edit/<choice>/assign - displayEditNextSlide - containerID of slide choice resides on - Assignment will be done via a form rather than URL.
#adventure->Slide->ChoiceContainer->Choice->NextSlide

def getUnconfiguredSlides(adventure):
    unconfiguredSlides = []
    slideSet = adventure.slide_set.all()
    for eachSlideSet in slideSet:
        if eachSlideSet.winningSlide==False and (len(models.NextSlide.objects.all().filter(nextSlide = eachSlideSet)) != 0 or eachSlideSet.startSlide==True):
            choiceContainer = models.ChoiceContainer.objects.all().filter(curSlide=eachSlideSet)[0]
            if len(choiceContainer.choice_set.all()) == 0:
                unconfiguredSlides.append((eachSlideSet, choiceContainer, adventure))
            else:
                for eachChoice in choiceContainer.choice_set.all():
                    if len(models.NextSlide.objects.all().filter(fromChoice = eachChoice)) == 0:
                        unconfiguredSlides.append((eachSlideSet, choiceContainer, adventure))
                        break
    return unconfiguredSlides           

def getUnlinkedSlides(adventure):
    unlinkedSlides = []
    slideSet = adventure.slide_set.all()
    for eachSlide in slideSet:
        choiceContainer = models.ChoiceContainer.objects.all().filter(curSlide=eachSlide)[0]
        if eachSlide.startSlide != True and len(models.NextSlide.objects.all().filter(nextSlide = eachSlide)) == 0:
            unlinkedSlides.append((eachSlide, choiceContainer, adventure))
    return unlinkedSlides

def checkWinningSlide(adventure):
    slideSet = list(adventure.slide_set.all().filter(winningSlide=True))
    if len(slideSet) > 0:
        return True
    else:
        return False

@login_required
def deleteAdventure(request, adventureID):
    adventure = models.AdventureContainer.objects.get(id = adventureID)
    if adventure.user == request.user:
        adventure.delete()
        return redirect("/create/adv/")
    else:
        return redirect("/")

@login_required
def displayEditAdventure(request, adventureID):
    adventure = models.AdventureContainer.objects.get(id = adventureID)
    if adventure.user == request.user:
        if adventure.published == True:
            adventure.flipPublished()
        if request.method=="POST":
            form = forms.editAdventureForm(request.POST, instance = adventure)
            if form.is_valid():
                data_Dict = form.cleaned_data
                adventure.editFromDict(data_Dict)                
                
                startSlide = adventure.slide_set.all().filter(startSlide=True)
                if len(startSlide) > 0:
                    containerID = models.ChoiceContainer.objects.get(curSlide=startSlide[0]).id
                    return redirect("/create/adv/" + str(adventureID) + "/edit/"+str(containerID) + "/edit")
                else:
                    return redirect("/create/adv/" + str(adventureID) + "/add")
        else:
            form = forms.editAdventureForm(instance = adventure)
        return render(request, "creator/editAdventure.html", context={"form":form, "adventure":adventureID})
    else:
        return redirect("")


@login_required
def displayNewAdventure(request):
    if request.method=="POST":
        form = forms.newAdventureForm(request.POST)
        if form.is_valid():
            data_Dict = form.cleaned_data
            data_Dict["user"] = request.user
            newAdventure = models.AdventureContainer.createFromDict(data_Dict)
            return redirect("/create/adv/" + str(newAdventure.id) + "/add")
    else:
        form = forms.newAdventureForm()
    return render(request, "creator/editAdventure.html", context={"form":form})

#How to configure NextSlide -> Give choices for Slides to pick. Once Picked Use Form to get Slide Id and URL to get choice ID.
#We need prior ID to get back to the editSlideForm
@login_required
def displayEditNextSlide(request, adventureID, priorContainerID, fromChoiceID):
    adventure = models.AdventureContainer.objects.get(id = adventureID)
    if adventure.user == request.user:
        editNextSlide = models.NextSlide.objects.get(fromChoice = fromChoiceID)
        if request.method == "POST":
            form = forms.editNextSlide(request.POST, instance=editNextSlide)
            if form.is_valid():
                data_Dict = form.cleaned_data
                models.NextSlide.editFromDict(data_Dict, editNextSlide.id)
                return redirect("/create/adv/" + str(adventureID) + "/edit/" + str(priorContainer.id) + "/edit")
        else:
            form = forms.editNextSlide(request.POST, instance=editNextSlide)
        return render(request, "creator/edit.html", context={"form":form})
    else:
        return redirect("")

@login_required
def displayNewSlide(request, adventureID, priorContainerID=None, fromChoiceID=None):
    adventure = models.AdventureContainer.objects.get(id = adventureID)
    if adventure.user == request.user:
        if request.method=="POST":
            form = forms.newSlideForm(request.POST)
            if form.is_valid():
                data_Dict = form.cleaned_data
                newSlide = models.Slide.createFromDict(data_Dict, adventure)
                oldChoiceContainer = None
                prevSlide = newSlide
                if priorContainerID != None:
                    oldChoiceContainer = models.ChoiceContainer.objects.get(id=priorContainerID)
                    prevSlide = oldChoiceContainer.curSlide
                if fromChoiceID != None:
                    #Assign the new slide to a choice.
                    fromChoice = models.Choice.objects.get(id=fromChoiceID)
                    dataDict = {"nextSlide":newSlide, "fromChoice":fromChoice}
                    newnextSlide = models.NextSlide.createFromDict(dataDict)
                #Create New Container to store choices.
                newChoiceContainer = models.ChoiceContainer.createFromObj(newSlide, prevSlide)
                return redirect("/create/adv/" + str(adventureID) + "/edit/"+str(newChoiceContainer.id) + "/edit")
        else:
            form = forms.newSlideForm()
        return render(request, "creator/newSlide.html", context={"form":form, "adventureID":adventureID, "choiceID":priorContainerID})
    else:
        return redirect("")


@login_required
def displayLinkSlide(request, adventureID, priorContainerID=None, fromChoiceID=None):
    adventure = models.AdventureContainer.objects.get(id = adventureID)
    if adventure.user == request.user:
        if request.method=="POST":
            form = forms.linkSlide(request.POST)
            slideSelection = models.Slide.objects.all().filter(adventureContainer=adventure)
            slideSelection = slideSelection.exclude(id=models.ChoiceContainer.objects.get(id=priorContainerID).curSlide.id)
            choices = []
            for eachSelection in slideSelection:
                choices.append((eachSelection.id, eachSelection))
            form.fields["curSlide"].choices = choices
            if form.is_valid():
                data_Dict = form.cleaned_data
                print(data_Dict["curSlide"])
                curSlide = models.Slide.objects.get(id=data_Dict["curSlide"])
                fromChoice = models.Choice.objects.get(id = fromChoiceID)
                nextSlide = None
                try:
                    nextSlide = models.NextSlide.objects.get(fromChoice=fromChoice)
                    nextSlide.nextSlide = curSlide
                    nextSlide.save()
                    print("This:" + str(nextSlide.nextSlide))
                    print("Try Block")
                except:
                    nextSlide = models.NextSlide.objects.get_or_create(fromChoice=fromChoice, nextSlide=curSlide)
                    print("Exception Met")
                fromChoice.pathAssigned=True
                fromChoice.save()
                return redirect("/create/adv/" + str(adventureID) + "/edit/"+str(priorContainerID) + "/edit")
        else:
            form = forms.linkSlide()
            slideSelection = models.Slide.objects.all().filter(adventureContainer=adventure)
            slideSelection = slideSelection.exclude(id=models.ChoiceContainer.objects.get(id=priorContainerID).curSlide.id)
            if len(slideSelection) == 0:
                return redirect("/create/adv/" + str(adventureID) + "/add/" + str(priorContainerID) + "/add/" + str(fromChoiceID) + "/assign")
            choices = []
            for eachSelection in slideSelection:
                choices.append((eachSelection.id, eachSelection))
            form.fields["curSlide"].choices = choices
        return render(request, "creator/newSlide.html", context={"form":form, "adventureID":adventureID, "choiceID":priorContainerID})
    else:
        return redirect("")


@login_required
def deleteSlide(request, adventureID, containerID):
    adventure = models.AdventureContainer.objects.get(id = adventureID)
    if adventure.user == request.user:
        container = models.ChoiceContainer.objects.get(id=containerID)
        slide = adventure.slide_set.get(id = container.curSlide.id)
        prevSlide = adventure.slide_set.get(id = container.prevSlide.Slide.id)
        prevContainerId = models.ChoiceContainer.objects.get(curSlide = prevSlide).id
        slide.delete()
        return redirect("/create/adv/" + str(adventureID) + "/edit/" + str(prevContainerId) + "/edit")
    else:
        return redirect("")


@login_required
def displayEditSlide(request, adventureID, containerID):
    adventure = models.AdventureContainer.objects.get(id = adventureID)
    if adventure.user == request.user:
        adventure.published = False
        adventure.save()
        slide = adventure.slide_set.get(id = models.ChoiceContainer.objects.get(id=containerID).curSlide.id)
        container = models.ChoiceContainer.objects.get(id=containerID)
        choices = container.choice_set.all()
        choice_Tuple = []
        goBackContainer = None
        if slide.startSlide == False:
            goBackContainer = models.ChoiceContainer.objects.get(curSlide=container.prevSlide.Slide)
            print(goBackContainer)
        for eachChoice in choices:
            try:
                choice_Tuple.append((eachChoice, models.ChoiceContainer.objects.get(curSlide=models.NextSlide.objects.get(fromChoice = eachChoice).nextSlide)))
            except exceptions.ObjectDoesNotExist:
                choice_Tuple.append((eachChoice, None))
            print(eachChoice.pathAssigned)
        unconfiguredSlides = getUnconfiguredSlides(adventure)
        unlinkedSlides = getUnlinkedSlides(adventure)
        if request.method=="POST":
            form = forms.editSlideForm(request.POST, instance=slide)
            if form.is_valid():
                data_Dict = form.cleaned_data
                editSlide = models.Slide.editFromDict(data_Dict, slide.id)
                return redirect("/create/adv/" + str(adventureID) + "/edit/"+str(containerID) + "/edit")
        else:
            form = forms.editSlideForm(instance=slide)
            #Eventually grab all unconfigured choices in choice_container so they can be displayed.
            return render(request, "creator/editSlide.html", context={"form":form, "adventure":adventure, "curSlide":slide, "container":container, "choices":choice_Tuple, "unconfiguredSlides":unconfiguredSlides, "unlinkedSlides":unlinkedSlides,"goBack":goBackContainer, "winningSlide":checkWinningSlide(adventure)})

    else:
        return redirect("")

@login_required
def displayNewChoice(request, adventureID, containerID):
    adventure = models.AdventureContainer.objects.get(id = adventureID)
    if adventure.user == request.user:
        if request.method=="POST":
            form = forms.newChoiceForm(request.POST)
            if form.is_valid():
                data_Dict = form.cleaned_data
                data_Dict["choiceContainer"] = models.ChoiceContainer.objects.get(id=containerID)
                newChoice = models.Choice.addChoice(data_Dict)
                return redirect("/create/adv/" + str(adventureID) + "/edit/"+str(containerID) + "/edit")
        else:
            form = forms.newChoiceForm()
        return render(request, "creator/editAdventure.html", context={"form":form})
    else:
        return redirect("")


@login_required 
def displayEditChoice(request, adventureID, containerID, choiceID):
    adventure = models.AdventureContainer.objects.get(id = adventureID)
    editChoice = models.Choice.objects.get(id=choiceID)
    if adventure.user == request.user:
        if request.method == "POST":
            form = forms.editChoiceForm(request.POST, instance = editChoice)
            if form.is_valid():
                data_Dict = form.cleaned_data
                editChoice = models.Choice.editChoice(data_Dict, choiceID)
                return redirect("/create/adv/" + str(adventureID) + "/edit/"+str(containerID) +"/edit")
        else:
            form = forms.editChoiceForm(instance = editChoice)
        return render(request, "creator/editAdventure.html", context={"form":form})
    else:
        return redirect("")


@login_required
def deleteChoice(request, adventureID, containerID, choiceID):
    adventure = models.AdventureContainer.objects.get(id=adventureID)
    if adventure.user == request.user:
        deleteChoice = models.Choice.objects.get(id=choiceID)
        deleteChoice.delete()
        return redirect("/create/adv/" + str(adventureID) + "/edit/"+str(containerID) + "/edit")
    else:
        return redirect("")

@login_required
def submitAdventure(request, adventureID):
    adventure = models.AdventureContainer.objects.get(id=adventureID)
    if adventure.user == request.user:
        adventure.published = True
        adventure.save()
        return redirect("/")
    else:
        return redirect("/")

@login_required
def viewCreationDashboard(request):
    publishedUserAdventures=models.AdventureContainer.objects.all().filter(user = request.user, published=True)
    unpubblishedUserAdventures=models.AdventureContainer.objects.all().filter(user = request.user, published=False)
    return render(request,"creator/dashboard.html", context={"username":request.user.username, "PA": publishedUserAdventures, "UA": unpubblishedUserAdventures})

    
    