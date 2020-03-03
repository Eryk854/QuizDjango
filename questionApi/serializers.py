from .models import Question, SuggestQuestion
from user.models import Player
from rest_framework import serializers


class QuestionSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Question
        fields = '__all__'


class QuestionUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Question
        fields = ['text', 'answerA', 'answerB', 'answerC', 'answerD']


class SuggestQuestionSerializer(serializers.HyperlinkedModelSerializer):
    player = serializers.PrimaryKeyRelatedField(
        queryset=Player.objects.all()
    )
    class Meta:
        model = SuggestQuestion
        #fields = '__all__'
        #fields = ['url', 'text', 'player']
        exclude = ('status',)
