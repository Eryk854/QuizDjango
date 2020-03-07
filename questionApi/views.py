from django.shortcuts import render, redirect
from django.core import serializers

from rest_framework import viewsets, mixins
from rest_framework import permissions, authentication
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveDestroyAPIView
from rest_framework.mixins import DestroyModelMixin
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView

from .permissions import MyPermission
from .serializers import QuestionSerializer, QuestionUserSerializer, SuggestQuestionSerializer
from .models import Question, SuggestQuestion
from user.models import Account

import requests


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    # I also create my own permission class witch do the same as get_permission method permission_classes = [MyPermission]
    #authentication_classes = [authentication.RemoteUserAuthentication]
    authentication_classes = [authentication.TokenAuthentication,
                              authentication.SessionAuthentication]

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


class SuggestQuestionVieSet(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            # mixins.DestroyModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.CreateModelMixin,
                            mixins.UpdateModelMixin):
    serializer_class = SuggestQuestionSerializer
    queryset = SuggestQuestion.objects.filter(status='Wait')
    permission_classes = [permissions.IsAdminUser]
    authentication_classes = [authentication.TokenAuthentication,
                              authentication.SessionAuthentication]

    @action(detail=True, methods=['get'])
    def confirm_question(self, request, pk=None):
        """
        This function confirm and add suggest question from user to list of question used in quiz app.
        If question has already been confirmed return this messege
        """
        serializer = SuggestQuestionSerializer(SuggestQuestion.objects.get(pk=pk), context={'request': request})
        data = serializer.data
        data.pop('url')
        data.pop('player')
        token = Token.objects.get(user_id=request.user.id)
        s_question = SuggestQuestion.objects.get(text=data['text'])
        if s_question.status == 'Wait':
            s_question.status = 'Added'
            s_question.save()
            # add to question api
            headers = {'content-type': 'application/json', 'Authorization': 'Token {}'.format(token)}
            requests.post("http://localhost:8000/api/question/", headers=headers, json=data)
            return redirect("suggestquestion-list")
        else:
            return Response("Question has already been confirmed")

    @action(detail=True, methods=['get'])
    def delete_question(self, request, pk=None):
        serializer = SuggestQuestionSerializer(SuggestQuestion.objects.get(pk=pk), context={'request': request})
        data = serializer.data
        s_question = SuggestQuestion.objects.get(text=data['text'])
        if s_question.status == 'Wait':
            s_question.status = 'Deleted'
            s_question.save()
            return redirect("suggestquestion-list")
        else:
            return Response("Question has already been confirmed ")

    @action(detail=False, methods=['get'])
    def deleted_list(self, request):
        serializer = SuggestQuestionSerializer(SuggestQuestion.objects.filter(status="Deleted"),
                                               context={'request': request}, many=True)
        data = serializer.data

        return Response(data)

    @action(detail=False, methods=['get'])
    def added_list(self, request):
        serializer = SuggestQuestionSerializer(SuggestQuestion.objects.filter(status="Added"),
                                               context={'request': request}, many=True)
        data = serializer.data

        return Response(data)

    # @action(detail=False, methods=['get'])
    # def question_status(self, request):
    #
    #     added = SuggestQuestion.objects.filter(player=request.user.id, status="Added").count()
    #     deleted = SuggestQuestion.objects.filter(player=request.user.id, status="Deleted").count()
    #     waiting = SuggestQuestion.objects.filter(player=request.user.id, status="waiting").count()
    #
    #     return Response({'added': added, 'deleted': deleted, 'waiting': waiting})


class QuestionStatusView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication,
                              authentication.SessionAuthentication]

    def get(self, request):
        print(request.user.id)
        added = SuggestQuestion.objects.filter(player=request.user.id, status="Added").count()
        deleted = SuggestQuestion.objects.filter(player=request.user.id, status="Deleted").count()
        waiting = SuggestQuestion.objects.filter(player=request.user.id, status="Wait").count()

        return Response({'added': added, 'deleted': deleted, 'waiting': waiting})

