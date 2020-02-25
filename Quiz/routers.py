from questionApi.views import QuestionViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('question', QuestionViewSet, basename='question')