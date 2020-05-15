from django.shortcuts import render, redirect
from django.core import exceptions
from creator import models
from .models import Player, UserStatistics
from django.contrib.auth.decorators import login_required
from . import forms

@login_required
def playAdventure(request, adventureID):
    adventure = models.AdventureContainer.objects.get(id=adventureID)
    adventure.timesPlayed = adventure.timesPlayed + 1
    adventure.save()
    startSlide = adventure.slide_set.all().filter(startSlide=True)[0]
    player = Player.objects.get_or_create(user=request.user)[0]
    player.checkPoint = startSlide
    player.checkPointSet = True
    player.health = 100
    player.save()
    playerStats = UserStatistics.objects.get_or_create(user=request.user, adventure=adventure)[0]
    playerStats.timesPlayed = playerStats.timesPlayed + 1
    playerStats.save()
    choiceContainer = models.ChoiceContainer.objects.get(curSlide=startSlide)
    choices = choiceContainer.choice_set.all()
    return redirect("/play/" + adventure.title.replace(" ", "_"))
    #Depending on the choice selected get the next slide and render again.
@login_required
def viewSlide(request, adventureName):
    try:
        player = Player.objects.get(user=request.user)
    except exceptions.ObjectDoesNotExist:
        return redirect("/") #send those cheaters back to the dashboard - they didn't start from square 1.
    if player.checkPointSet == False:
        return redirect("/") #send those cheaters back to the dashboard - they didn't start from square 1.
    slide = player.checkPoint
    adventure = slide.adventureContainer
    choices = models.ChoiceContainer.objects.get(curSlide=slide).choice_set.all()
    if request.method == "POST":
        choiceSelection = request.POST.get("choice", False)
        if choiceSelection==False:
            return render(request, "player/player.html", context={"health":player.health,"adventure":adventure,"slide":slide, "choices":choices})
        choiceContainer = models.ChoiceContainer.objects.get(curSlide=slide)
        choice = choiceContainer.choice_set.get(text=choiceSelection)
        newSlide = models.NextSlide.objects.get(fromChoice = choice).nextSlide
        if player.health == 100 and choice.healthChange > 0:
            pass
        else:
            player.health = player.health + choice.healthChange
       
        if player.health <= 0:
            playerStats = UserStatistics.objects.get_or_create(user=request.user, adventure=adventure)[0]
            playerStats.timesLost = playerStats.timesLost + 1
            playerStats.save()
            adventure.timesLost = adventure.timesLost + 1
            adventure.save()
            return render(request, "player/loser.html", context={"health": 0, "adventure":adventure}) 
        
        if newSlide.winningSlide:
            playerStats = UserStatistics.objects.get_or_create(user=request.user, adventure=adventure)[0]
            playerStats.timesWon = playerStats.timesWon + 1
            if playerStats.highestWinningHealth < player.health:
                playerStats.highestWinningHealth = player.health
            playerStats.save()
            adventure.timesWon = adventure.timesWon + 1
            adventure.save()
            
            
        player.checkPoint = newSlide
        player.save()
        return redirect("/play/" + adventure.title.replace(" ", "_"))
    return render(request, "player/player.html", context={"health":player.health,"adventure":adventure,"slide":slide, "choices":choices})

@login_required
def endGame(request, adventureName):
    try:
        player = Player.objects.get(user=request.user)
    except exceptions.ObjectDoesNotExist:
        return redirect("/") #send those cheaters back to the dashboard - they didn't start from square 1.
    player.delete()
    return redirect("/")

@login_required      
def viewStatistics(request):
    personalStatList = UserStatistics.objects.all().filter(user=request.user)
    GenericList = models.AdventureContainer.objects.all().filter(published=True).order_by("timesPlayed")[:5]
    return render(request, "player/stats.html", context={"personalStats": personalStatList, "GenericList": GenericList})

# Create your views here.
