from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate as DJauthenticate
from django.contrib.auth import login as DJlogin
from django.contrib.auth import logout as DJlogout
from . import forms

#-------------------LOGIN/NEWUSER FUNCTIONS------------------------------------
def displayLogin(request, msgCode = 0):
    errorMsg = None
    otherMsg = None
    if request.method == "POST":
        print(request.POST)
        form = forms.LoginForms.newLogin(request.POST)
        print(form)
        if form.is_valid():
            print(form.is_valid())
            login_Dict = form.cleaned_data
            return login(request, login_Dict)
    else:
        form = forms.LoginForms.newLogin()
    if msgCode == 1:
        errorMsg = "Invalid Login Credentials"
    elif msgCode == 2:
        otherMsg = "New Account Succesfully Created"
    elif msgCode == 3:
        errorMsg = "A Login Is Required To View This Page"
    return render(request, "dashboard/login.html", context={"form":form, "errorMsg":errorMsg, "otherMsg":otherMsg, "newAccount":True})

def login(request, login_Dict):
    user = DJauthenticate(username=login_Dict["username"].upper(), password=login_Dict["password"])
    if user is not None:
        DJlogin(request, user)
        return redirect("/")
    else:
        return redirect("/login/1") #displayLogin(request, reset=True, errorMSG="Invalid login credentials")
    
def displayNewAccount(request):
    otherMsg = None
    if request.method == "POST":
        form = forms.newUser(request.POST)
        if form.is_valid():
            data_Dict = form.cleaned_data
            User.objects.create_user(username = data_Dict["username"].upper(),
                                    first_name = data_Dict["first_name"],
                                    last_name = data_Dict["last_name"],
                                    email = data_Dict["email"].lower(),
                                    password = data_Dict["password"])
            return redirect("/login/2")
    else:
        form = forms.newUser()
    return render(request, "dashboard/login.html", context={"form":form, "otherMsg":otherMsg})

#----------------------------------------------------------------------------------------------------
#----------------------------------Dashboard---------------------------------------------------------
def viewDashboard(request):
    return HttpResponse("Dashboard temp view.")
    