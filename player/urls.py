from django.urls import path
from . import views

#urls should assumed to have the prefix /play .. See cyoa.urls.py
urlpatterns = [
    path('<int:adventureID>', views.playAdventure, name="Play Adventure"),
    path('<str:adventureName>', views.viewSlide, name="View Slide"),
    path('<str:adventureName>/end', views.endGame, name="End Game"),
    path('stats/', views.viewStatistics, name="Statistics")
]