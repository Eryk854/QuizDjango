from django.urls import path

from user.backends import SocialBackend
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from .views import UserUpdateView, UserEditView, RegisterUserView
from . import views as user_view

urlpatterns = [
    path('',user_view.index, name="login_page"),
    #path('',SocialBackend),
    path('our_login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name="our_login"),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout_page.html'), name="logout"),
    path('user_panel', user_view.user_panel, name="user_panel"),
    path('user_panel/edit_profile/', UserEditView.as_view()),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('send', user_view.send),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)