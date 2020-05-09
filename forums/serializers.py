from .models import Messages
from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model  = User
    fields = ['username','email']

class MessageSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    author = UserSerializer()
    model  = Messages
    fields = '__all__'
    read_only_fields = ['author','edited']