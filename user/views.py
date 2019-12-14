from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from .models import Player
from .forms import RegisterForm
from django.contrib import messages
import jwt
from django.contrib.auth import login,authenticate
from random import randint
# Create your views here.


def index(request):
    user = authenticate(request=request)
    if user:
        login(request,user)
        return redirect("Quiz/")
    else:
        return render(request, "Users/login_page.html")


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Konto zostało stworzone dla {}!".format(form.cleaned_data['email']))
            return redirect("our_login")
    else:
        form = RegisterForm

    return render(request,"registration/register.html",{'form':form})
