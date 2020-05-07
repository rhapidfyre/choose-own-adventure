from django import forms
from django.forms import ModelForm
from . import models

class newAdventureForm(forms.Form):
    title = forms.CharField(max_length=100, label="Name Your Adventure", widget=forms.TextInput(attrs={"class":"form-control form-control-lg"}))

class editAdventureForm(ModelForm):
    class Meta:
        models = models.AdventureContainer
        fields = ["title"]
        labels = {
            "title":"Name Your Adventure"
        }
        widgets = {
            "title": forms.TextInput(attrs={"class":"form-control form-control-lg"})
            }

class newSlideForm(forms.Form):
    text = forms.CharField(max_length=256, label="text", widget=forms.Textarea(attrs={"class":"form-control form-control-lg text-center"}))
    winningSlide = forms.ChoiceField(label="Slide Outcome", choices=[(False,"Continue" ),(True, "Winning Slide - End Game On Slide")], widget=forms.Select(attrs={"class":"form-control form-control-lg text-center"}))

class editSlideForm(ModelForm):
    class Meta:
        model = models.Slide
        fields = ["text", "winningSlide"]
        labels = {
            "winningSlide":"Slide Outcome"
        }
        widgets = {
            "text" : forms.Textarea(attrs={"class":"form-control form-control-lg text-center"}),
            "winningSlide" :  forms.Select(attrs={"class":"form-control form-control-lg"}, choices=[(False, "Continue"), (True, "Winning Path - End Game On Slide")])
        }

class newChoiceForm(forms.Form):
    text = forms.CharField(max_length=50, label="Choice Text", widget=forms.Textarea(attrs={"class":"form-control form-control-lg"}))
    healthChange = forms.IntegerField(label="Health Change", widget=forms.NumberInput(attrs={"class":"form-control form-control-lg"}))

class editChoiceForm(ModelForm):
    class Meta:
        model = models.Choice
        fields = ['text', 'healthChange']
        labels = {
            "text":"Choice Text",
        }
        widgets = {
            'text':forms.Textarea(attrs={"class":"form-control form-control-lg"}),
            'healthChange':forms.NumberInput(attrs={"class":"form-control form-control-lg"})
        }
    
class editNextSlide(ModelForm):
    class Meta:
        model = models.NextSlide
        fields = ["nextSlide"]
        widgets = {forms.Select(attrs={"class":"form-control form-control-lg"})}
                  
class newNextSlide(forms.Form):
    nextSlide = forms.ChoiceField(label="Next Slide", widget=forms.Select(attrs={"class":"form-control form-control-lg"}))
    
class linkSlide(forms.Form):
    curSlide = forms.ChoiceField(label="Select Slide to Link to This Choice", widget=forms.Select(attrs={"class":"form-control form-control-lg text-center"}))
    
    def clean(self):
       cleaned_data = super().clean()
       data = cleaned_data.get("curSlide")