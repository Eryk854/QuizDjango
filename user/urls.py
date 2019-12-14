from django.urls import path
from . import views
from user.backends import SocialBackend
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('',views.index, name="login_page"),
    #path('',SocialBackend),
    path('our_login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name="our_login"),
    path('logout/',auth_views.LogoutView.as_view(template_name='registration/logout_page.html'), name="logout")
]