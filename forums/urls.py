
from django.urls import path
from . import views

urlpatterns = [
    path('', views.displayForums),
    path('thread/', views.displayThread)
]