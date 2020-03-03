from questionApi.views import QuestionViewSet, SuggestQuestionVieSet
from rest_framework import routers

# router = routers.DefaultRouter()
# router.register('question', QuestionViewSet, basename='question')
#
# suggest_router = routers.DefaultRouter()
# suggest_router.register('suggest_question', SuggestQuestionVieSet)
#suggest_router.register('deleted_question', DeletedQuestionView)
router = routers.DefaultRouter()
router.register('question', QuestionViewSet)
router.register('suggest_question', SuggestQuestionVieSet)