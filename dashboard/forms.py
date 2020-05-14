from django import forms
from django.forms import ModelForm
from . import models
from django.contrib.auth.models import User

class LoginForms():
    class newLogin(forms.Form):
        username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={"class":"form-control form-control-lg"}))
        password = forms.CharField(label="Password", max_length=50, widget=forms.PasswordInput(attrs={"class":"form-control form-control-lg"}))

class newUser(forms.Form):
    username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={"class":"form-control form-control-lg"}))
    first_name = forms.CharField(label="First Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control form-control-lg"}))
    last_name = forms.CharField(label="Last Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control form-control-lg"}))
    email = forms.CharField(label="Email", max_length=50, widget=forms.TextInput(attrs={"class":"form-control form-control-lg"}))
    password = forms.CharField(label="Password", max_length=50, widget=forms.PasswordInput(attrs={"class":"form-control form-control-lg"}))
    
    def clean(self):
        cleaned_data = super().clean()
        if len(User.objects.all().filter(username = cleaned_data["username"].upper())):
            self.add_error('username', "Username Already In Use")
        if len(User.objects.all().filter(email = cleaned_data["email"].lower())):
            self.add_error('email', "Email Already In Use")
 