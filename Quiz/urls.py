"""Quiz URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path,include
from user import views as user_view
from questionApi import views as api_views
from user.views import RegisterUserView
from .routers import router#, suggest_router

urlpatterns = [
    path('admin/', admin.site.urls),
    path('Quiz/', include("Pytania.urls")),
    path('', include("user.urls")),
    path('register/', RegisterUserView.as_view(), name="register_user"),
    path('api/', include(router.urls), name="question_api"),
    path('api/questions_status/', api_views.QuestionStatusView.as_view()),

    # path('password_reset/', auth_views.password_reset, name='password_reset'),
    # path('password_reset/done/', auth_views.password_reset_done, name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', auth_views.password_reset_confirm, name='password_reset_confirm'),
    # path('reset/done/', auth_views.password_reset_complete, name='password_reset_complete'),
    #path('suggest/', include(suggest_router.urls)),




]
