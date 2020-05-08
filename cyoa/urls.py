"""cyoa URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from creator import urls as creatorUrls
from dashboard import urls as dashboardUrls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('create/adv/', include(creatorUrls)),
    path('', include(dashboardUrls)),
    path('', views.displayNewAdventure),
    path('<int:adventureID>/add', views.displayNewSlide),
    path('<int:adventureID>/add/<int:priorContainerID>/add/<int:fromChoiceID>/assign', views.displayNewSlide),
    path('<int:adventureID>/add/<int:priorContainerID>/add/<int:fromChoiceID>/link', views.displayLinkSlide),
    path('<int:adventureID>/add/<int:containerID>/add', views.displayNewChoice),
    path('<int:adventureID>/edit/<int:containerID>/edit', views.displayEditSlide),
    path('<int:adventureID>/edit/<int:containerID>/delete', views.deleteSlide),
    path('<int:adventureID>/edit/<int:containerID>/edit/<int:choiceID>', views.displayEditChoice),
    path('<int:adventureID>/edit/<int:priorContainerID>/edit/<int:fromChoiceID>/assign', views.displayEditNextSlide),
    path('<int:adventureID>/edit/<int:containerID>/edit/<int:choiceID>/delete', views.deleteChoice),
    path('<int:adventureID>/submit', views.submitAdventure),
    path('', views.viewDashboard, name="Dashboard"),
    path('login/', views.displayLogin, name="Login"),
    path('login/<int:msgCode>', views.displayLogin, name="Login With Warning"),
    path("newAccount/", views.displayNewAccount, name="New Account"),
    path("logout/", views.logout, name="logout"),
]
