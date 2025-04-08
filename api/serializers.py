from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model


User = get_user_model()



class UserRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name','email', 'phoneNumber', 'password']
        extra_kwargs = {'password': {'write_only': True}, }

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True)




class QuestionSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'user', 'title', 'created_at']
        read_only_fields = ['user', 'created_at']


class AnswerSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Answer
        fields = ['id', 'user', 'content', 'created_at', 'likes_count']
        read_only_fields = ['user', 'created_at', 'likes_count', 'question']

    def get_likes_count(self, obj):
        return obj.likes.count()