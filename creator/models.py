from django.db import models
from django.contrib.auth.models import User

#Describing ForeignKey relationships - Giving the parent class the _set functionality to grab objects who link to it via foreignkey.
#AdventureContainers have sets of Slides
#Slides have A Choice Container and a GoBack(A GoBack will have the same ChoiceContainer foreign key if it's referencing a starting slide.) - Also NextSlide Classes
#ChoiceContainers have sets of choices
#Choices have a NextSlide

class AdventureContainer(models.Model):
    title = models.CharField(max_length=100)
    published = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete = models.SET_NULL, null=True) #Stores first_name, last_name, username, password

    
    def createFromDict(data_Dict):
        newAdventure = AdventureContainer.objects.create(title=data_Dict["title"], user=data_Dict["user"])
        return newAdventure
    
    def editFromDict(id, data_Dict):
        editAdventure = AdventureContainer.objects.get(id=id)
        editAdventure.title = data_Dict["title"]
        editAdventure.save()
        return editAdventure
        
    def flipPublished(id):
        editAdventure = AdventureContainer.objects.get(id=id)
        if editAdventure.published == True:
            editAdventure.published = False
        else:
            editAdventure.published = True
        return editAdventure
    
class Slide(models.Model):
    startSlide = models.BooleanField(default=False)
    text = models.CharField(max_length=256)
    adventureContainer = models.ForeignKey(AdventureContainer, on_delete=models.CASCADE) 
    winningSlide = models.BooleanField(default=False)
    
    def __str__(self):
        return self.text
    
    def createFromDict(data_Dict, adventure):
        startSlide = False
        if len(adventure.slide_set.all()) == 0:
            startSlide = True
        newSlide = Slide.objects.create(text=data_Dict["text"], winningSlide=data_Dict["winningSlide"], startSlide=startSlide, adventureContainer=adventure)
        return newSlide
    
    def editFromDict(data_Dict, id):
        editSlide = Slide.objects.get(id=id)
        editSlide.text = data_Dict["text"]
        editSlide.winningSlide = data_Dict["winningSlide"]
        editSlide.save()
        return editSlide

class GoBack(models.Model):
    Slide = models.ForeignKey(Slide, on_delete=models.CASCADE)

class ChoiceContainer(models.Model):
    #If a slide is a starting slide curSlide = prevSlide
    curSlide = models.OneToOneField(Slide, on_delete=models.CASCADE, unique=True) #gives an existing Slide object slide.choicecontainer_set.all() functionality
    prevSlide = models.ForeignKey(GoBack, on_delete=models.CASCADE) #gives a slide the ability to reference the previous slide - for editing purposes.
    
    def createFromObj(curSlide, prevSlide):
        #data_Dict contains the number of choices we want in the container.
        if curSlide.startSlide == True:
            goBack = GoBack.objects.create(Slide=curSlide)
            return ChoiceContainer.objects.create(curSlide=curSlide, prevSlide=goBack)
        else:
            goBack = GoBack.objects.create(Slide=prevSlide)
            return ChoiceContainer.objects.create(curSlide=curSlide,prevSlide=goBack)

class Choice(models.Model):
    text = models.CharField(max_length=50)
    healthChange = models.IntegerField(default=0)
    choiceContainer = models.ForeignKey(ChoiceContainer, on_delete=models.CASCADE) #gives existing ChoiceContainer objects ChoiceContainer.choice_set.all() functionality
    pathAssigned = models.BooleanField(default=False)
    def addChoice(data_Dict):
        choiceContainer = data_Dict["choiceContainer"]
        if len(choiceContainer.choice_set.all()) != 4: #4 is the current maximum of choices alloud.
            newChoice = Choice.objects.create(text = data_Dict["text"],
                                      healthChange = data_Dict["healthChange"],
                                      choiceContainer = data_Dict["choiceContainer"])
            return newChoice

    def editChoice(data_Dict,id):
        editObject = Choice.objects.get(id=id)
        editObject.text = data_Dict["text"]      
        editObject.healthChange = data_Dict["healthChange"]
        editObject.save()
        return editObject  
    
class NextSlide(models.Model):
    nextSlide = models.ForeignKey(Slide, on_delete=models.CASCADE)
    fromChoice = models.OneToOneField(Choice, on_delete=models.CASCADE, unique=True)
    
    def createFromDict(data_Dict):
        newNextSlide = NextSlide.objects.create(nextSlide = data_Dict["nextSlide"], fromChoice = data_Dict["fromChoice"])
        data_Dict["fromChoice"].pathAssigned = True
        data_Dict["fromChoice"].save()
        return newNextSlide
        
    def editFromDict(data_Dict, id):
        editNextSlide = NextSlide.objects.get(id)
        editNextSlide.nextSlide = data_Dict["nextSlide"]
        editNextSlide.save()
        return editNextSlide
