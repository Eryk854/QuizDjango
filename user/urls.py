from django.urls import path
from . import views as user_view
from user.backends import SocialBackend
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import UpdateView
from .views import UserUpdateView, UserEditView, RegisterUserView

urlpatterns = [
    path('',user_view.index, name="login_page"),
    #path('',SocialBackend),
    path('our_login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name="our_login"),
    path('logout/',auth_views.LogoutView.as_view(template_name='registration/logout_page.html'), name="logout"),
    path('user_panel',user_view.user_panel, name="user_panel"),
    #path('user_panel/edit_profile/',user_view.user_edit),
    path('user_panel/edit_profile/', UserEditView.as_view())

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)