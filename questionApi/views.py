from django.shortcuts import render
from .models import Question
from django.core import serializers
from .serializers import QuestionSerializer, QuestionUserSerializer
from rest_framework import viewsets
from rest_framework import permissions, authentication
from rest_framework.response import Response
from .permissions import MyPermission


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    # I also create my own permission class witch do the same as get_permission method permission_classes = [MyPermission]
    authentication_classes = [authentication.SessionAuthentication]

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
            permission_classes = [permissions.IsAuthenticated]
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
