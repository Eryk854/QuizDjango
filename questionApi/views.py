from django.shortcuts import render
from .models import Question, SuggestQuestion
from django.core import serializers
from .serializers import QuestionSerializer, QuestionUserSerializer, SuggestQuestionSerializer
from rest_framework import viewsets, mixins
from rest_framework import permissions, authentication
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveDestroyAPIView
from rest_framework.mixins import DestroyModelMixin
from rest_framework.decorators import action
from .permissions import MyPermission
from .authentication import MyAuthentication
import requests


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    # I also create my own permission class witch do the same as get_permission method permission_classes = [MyPermission]
    #authentication_classes = [authentication.RemoteUserAuthentication]
    authentication_classes = [authentication.TokenAuthentication]

    def get_permissions(self):
        """
        Only admin can create, delete, edit questions and display questions with answer
        App users can see questions without answer
        Not logged user don't see anything
        :return: permission list
        """
        if self.action != 'list':
            permission_classes = [permissions.IsAdminUser]
        else:
            print('tu')
            print(self.request.headers)
            permission_classes = [permissions.IsAuthenticated]
            print(self.request.user)
        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):
        """
        Admin and users see a different page with questions
        :return: return site with right question list
        """
        if request.user.is_staff:
            # user is a superuser so we display question with correct answer
            serializer = QuestionSerializer(self.queryset, many=True, context={'request': request})
            return Response(serializer.data)
        else:
            serializer = QuestionUserSerializer(self.queryset, many=True)
            return Response(serializer.data)




class ListSugestQuestion(DestroyModelMixin, ListAPIView):
    queryset = SuggestQuestion.objects.all()
    serializer_class = QuestionUserSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_destroy(self, instance):
        pass


class SuggestQuestionVieSet(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.DestroyModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.CreateModelMixin):
    serializer_class = SuggestQuestionSerializer
    queryset = SuggestQuestion.objects.all()
    permission_classes = [permissions.IsAdminUser]

    @action(detail=True, methods=['get'])
    def confirm_question(self, request, pk=None):
        serializer = SuggestQuestionSerializer(SuggestQuestion.objects.get(pk=pk), context={'request': request})

        data = serializer.data
        data.pop('url')
        data.pop('player')
        print(data)
        headers = {"content-type": "application/json"}
        r = requests.post("http://localhost:8000/api/question/", json=data, headers=headers)
        print(r.json())
        requests.delete("http://localhost:8000/suggest/suggest_question/{}".format(pk))
        return Response("Dodano")

