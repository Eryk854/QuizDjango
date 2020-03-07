from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.views.generic import UpdateView
from django.views import View
from django.contrib.messages.views import SuccessMessageMixin

from rest_framework.authtoken.models import Token

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from .models import Player, Account
from .forms import RegisterForm, UpdateProfileForm

import requests
import jwt
import os

from random import randint


def index(request):
    user = authenticate(request=request)
    if not user.is_anonymous:
        login(request, user)
        return redirect("Quiz/")
    else:
        if request.GET.get('error'):
            messages.error(request, "Wystąpił problem z pobraniem twojego adresu email!!!")
        return render(request, "Users/login_page.html")


def get_question_stats_from_api(request):
    token = Token.objects.get(user=request.user)
    headers = {'Authorization': 'Token {}'.format(token)}
    r = requests.get("http://localhost:8000/api/questions_status/", headers=headers)
    print(r.json())
    return r.json()


def user_panel(request):
    player = Player.objects.get(email=request.user.email)
    date_joined = Account.objects.get(email=request.user.email).date_joined
    questions_stats = get_question_stats_from_api(request)
    return render(request, "Users/user_page.html",
                  {'player': player,
                   'date_joined': date_joined,
                   'question_stats': questions_stats})


class RegisterUserView(SuccessMessageMixin, View):
    model = Account
    form = RegisterForm
    template = "registration/register.html"
    success_message = "Konto zostało stworzone dla %(email)s!"

    def get(self, request):

        return render(request, self.template, {'form': self.form})

    def post(self,request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Konto zostało stworzone dla {}!".format(form.cleaned_data['email']))
            return redirect("our_login")
        return render(request, self.template, {'form':form})


# poniżej widok edycji konta użytkownika w trzech wersjach
# Funkcyjny widok
def user_edit(request):
    player = Player.objects.get(email=request.user.email)
    if request.method == 'POST':
        update_form = UpdateProfileForm(request.POST, request.FILES, instance=player)
        if update_form.is_valid():
            update_form.save()
            messages.success(request, "Zaktualizowaliśmy twój profil!")
            return redirect('user_panel')
    else:
        update_form = UpdateProfileForm(instance=player)

    return render(request, "Users/user_update.html",
                  {'player': player,
                   'update_form':update_form})


# Widok oparty na dowolnej klasie
class UserEditView(View):
    model = Player
    form = UpdateProfileForm
    template = "Users/user_update.html"

    def get_object(self):
        return self.model.objects.filter(email=self.request.user.email).first()

    def get(self, request):
        player = UserEditView.get_object(self)
        update_form = self.form(instance=player)
        print(update_form)
        return render(request, self.template,
                  {'player': player,
                   'form': update_form})

    def post(self, request):
        player = UserEditView.get_object(self)
        update_form = UpdateProfileForm(request.POST, request.FILES, instance=player)
        if update_form.is_valid():
            update_form.save()
            messages.success(request, "Zaktualizowaliśmy twój profil!")
            return redirect('user_panel')

        self.get(request)


# Generyczny widok
class UserUpdateView(SuccessMessageMixin, UpdateView):
    model = Player
    form_class = UpdateProfileForm
    template_name = 'Users/user_update.html'
    success_message = "Zaktualizowaliśmy twój profil!"

    def get_object(self, queryset=None):
        return self.model.objects.filter(email=self.request.user.email).first()