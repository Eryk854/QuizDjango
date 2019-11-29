from django.urls import path
from . import views
urlpatterns = [
    path('',views.index, name="main-game-page"),
    path('inicialize/<str:email>',views.inicialize_user),
    path('start',views.pierwsze_pytanie),
    path('sprawdz_odp/<int:pytanie_id>',views.sprawdz_odp),
    path('kolejne_pytanie',views.kolejne_pytanie),
    path('zakoncz_quiz',views.zakoncz_quiz)
]