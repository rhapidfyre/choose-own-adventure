from .models import Messages, PostTags
from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model  = User
    fields = ['username','email']

class MessageSerializer(serializers.ModelSerializer):
  class Meta:
    author = UserSerializer()
    model  = Messages
    fields = '__all__'
    read_only_fields = ['author']

class PostTagsSerializer(serializers.ModelSerializer):
  class Meta:
    model  = PostTags
    fields = '__all__'