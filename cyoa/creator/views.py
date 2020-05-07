from django.shortcuts import render, redirect
from . import forms
from . import models
from django.core import exceptions

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

def displayNewAdventure(request):
    if request.method=="POST":
        form = forms.newAdventureForm(request.POST)
        if form.is_valid():
            data_Dict = form.cleaned_data
            newAdventure = models.AdventureContainer.createFromDict(data_Dict)
            return redirect("/create/adv/" + str(newAdventure.id) + "/add")
    else:
        form = forms.newAdventureForm()
    return render(request, "creator/editAdventure.html", context={"form":form})

#How to configure NextSlide -> Give choices for Slides to pick. Once Picked Use Form to get Slide Id and URL to get choice ID.
#We need prior ID to get back to the editSlideForm
def displayEditNextSlide(request, adventureID, priorContainerID, fromChoiceID):
    adventure = models.AdventureContainer.objects.get(id = adventureID)
    #If adventure.creator_name = request.user.username
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
    
def displayNewSlide(request, adventureID, priorContainerID=None, fromChoiceID=None):
    adventure = models.AdventureContainer.objects.get(id = adventureID)
    #If adventure.creator_name = request.user.username
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

def displayLinkSlide(request, adventureID, priorContainerID=None, fromChoiceID=None):
    adventure = models.AdventureContainer.objects.get(id = adventureID)
    #If adventure.creator_name = request.user.username
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
            return displayNewSlide(request, adventureID, priorContainerID, fromChoiceID)
        choices = []
        for eachSelection in slideSelection:
            choices.append((eachSelection.id, eachSelection))
        form.fields["curSlide"].choices = choices
    return render(request, "creator/newSlide.html", context={"form":form, "adventureID":adventureID, "choiceID":priorContainerID})

def deleteSlide(request, adventureID, containerID):
    adventure = models.AdventureContainer.objects.get(id = adventureID)
    #If adventure.creator_name == request.user.username
    container = models.ChoiceContainer.objects.get(id=containerID)
    slide = adventure.slide_set.get(id = container.curSlide.id)
    prevSlide = adventure.slide_set.get(id = container.prevSlide.Slide.id)
    prevContainerId = models.ChoiceContainer.objects.get(curSlide = prevSlide).id
    slide.delete()
    return redirect("/create/adv/" + str(adventureID) + "/edit/" + str(prevContainerId) + "/edit")

def displayEditSlide(request, adventureID, containerID):
    adventure = models.AdventureContainer.objects.get(id = adventureID)
    #If adventure.creator_name == request.user.username
    slide = adventure.slide_set.get(id = models.ChoiceContainer.objects.get(id=containerID).curSlide.id)
    container = models.ChoiceContainer.objects.get(id=containerID)
    choices = container.choice_set.all()
    choice_Tuple = []
    #Need to get prevslide choice container
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
    return render(request, "creator/editSlide.html", context={"form":form, "adventure":adventure, "container":container, "choices":choice_Tuple, "unconfiguredSlides":unconfiguredSlides, "unlinkedSlides":unlinkedSlides,"goBack":goBackContainer})

def displayNewChoice(request, adventureID, containerID):
    adventure = models.AdventureContainer.objects.get(id = adventureID)
    #If adventure.creator_name = request.user.username
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
    
def displayEditChoice(request, adventureID, containerID, choiceID):
    adventure = models.AdventureContainer.objects.get(id = adventureID)
    editChoice = models.Choice.objects.get(id=choiceID)
    #If adventure.creator_name = request.user.username
    if request.method == "POST":
        form = forms.editChoiceForm(request.POST, instance = editChoice)
        if form.is_valid():
            data_Dict = form.cleaned_data
            editChoice = models.Choice.editChoice(data_Dict, choiceID)
            return redirect("/create/adv/" + str(adventureID) + "/edit/"+str(containerID) +"/edit")
    else:
        form = forms.editChoiceForm(instance = editChoice)
    return render(request, "creator/editAdventure.html", context={"form":form})

def deleteChoice(request, adventureID, containerID, choiceID):
    adventure = models.AdventureContainer.objects.get(id=adventureID)
    #if adventure.creator_name = request.user.username:
    deleteChoice = models.Choice.objects.get(id=choiceID)
    deleteChoice.delete()
    return redirect("/create/adv/" + str(adventureID) + "/edit/"+str(containerID) + "/edit")
