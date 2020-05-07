from django.urls import path
from . import views

urlpatterns = [
    path('', views.viewDashboard, name="Dashboard"),
    path('login/', views.displayLogin, name="Login"),
    path('login/<int:msgCode>', views.displayLogin, name="Login With Warning"),
    path("newAccount/", views.displayNewAccount, name="New Account"),
]