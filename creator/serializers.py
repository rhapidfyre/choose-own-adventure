from .models import AdventureContainer
from .models import Slide
from .models import GoBack
from .models import ChoiceContainer
from .models import Choice
from .models import NextSlide
from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model  = User
    fields = ['username','email']

class AdventureSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    user = UserSerializer()
    model = AdventureContainer
    fields = '__all__'
    read_only_fields = ['user']

class SlideSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = GoBack
    fields = '__all__'

class GoBackSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = ChoiceContainer
    fields = '__all__'

class ChoiceContainerSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = ChoiceContainer
    fields = '__all__'

class ChoiceSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Choice
    fields = '__all__'

class NextSlideSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = NextSlide
    fields = '__all__'