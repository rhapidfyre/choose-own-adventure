from django.urls import path
from . import views

#urls should assumed to have the prefix /create/adv... See cyoa.urls.py
urlpatterns = [
    path('<int:adventureID>', views.playAdventure, name="Play Adventure"),
    path('<slug:adventureName>', views.viewSlide, name="View Slide"),
    path('<slug:adventureName>/end', views.endGame, name="End Game")
]