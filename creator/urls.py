
from django.urls import path
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'adventure', views.AdventureViewSet)
router.register(r'slide', views.SlideViewSet)
router.register(r'goback', views.GoBackViewSet)
router.register(r'choicecont', views.ChoiceContainerViewSet)
router.register(r'choice', views.ChoiceViewSet)
router.register(r'nextslide', views.NextSlideViewSet)

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
    path('<int:adventureID>/submit', views.submitAdventure),
]