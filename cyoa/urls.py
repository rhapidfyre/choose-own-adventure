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
from forums import urls as forumsUrls
from rest_framework import routers
from forums.views import MessageViewSet
from creator.views import AdventureViewSet
from creator.views import SlideViewSet
from creator.views import GoBackViewSet
from creator.views import ChoiceContainerViewSet
from creator.views import ChoiceViewSet
from creator.views import NextSlideViewSet


router = routers.DefaultRouter()
router.register(r'message', MessageViewSet)
router.register(r'adventure', AdventureViewSet)
router.register(r'slide', SlideViewSet)
router.register(r'goback', GoBackViewSet)
router.register(r'choicecont', ChoiceContainerViewSet)
router.register(r'choice', ChoiceViewSet)
router.register(r'nextslide', NextSlideViewSet)

urlpatterns = [
    path('', include(dashboardUrls)),
    path('forums/', include(forumsUrls)),
    path('admin/', admin.site.urls),
    path('create/adv/', include(creatorUrls)),
    path('api/v1/', include(router.urls)),
    path('api-auth/v1/', include('rest_framework.urls', namespace='rest_framework'))
]
