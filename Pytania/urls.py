from django.urls import path
from . import views
urlpatterns = [
    path('',views.index, name="main-game-page"),
    path('start',views.pierwsze_pytanie),
    path('sprawdz_odp/',views.sprawdz_odp, name="sprawdz_odp"),
    path('zakoncz_quiz',views.zakoncz_quiz, name="end_quiz"),
    path('questions/', views.questions),
    path('new_question/', views.AddNewQuestionView.as_view(), name='new_question'),
]