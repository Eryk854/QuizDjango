from .models import Question
from rest_framework import serializers


class QuestionSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Question
        fields = '__all__'


class QuestionUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Question
        fields = ['text', 'answerA', 'answerB', 'answerC', 'answerD']