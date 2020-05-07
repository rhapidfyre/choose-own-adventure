from django.urls import path
from . import views

#urls should assumed to have the prefix /create/adv... See cyoa.urls.py
urlpatterns = [
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
]