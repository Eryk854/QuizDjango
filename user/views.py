from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from .models import Player

import jwt
from random import randint
# Create your views here.

def index(request):
    from Pytania.views import flaga
    print(flaga)
    if not flaga:
        token = request.GET.get('token')
        print(token)
        if token:
            decode_jwt = jwt.decode(token, '926D96C90030DD58429D2751AC1BDBBC', algorithms='HS512',verify = False)
            user = Player.objects.filter(email=decode_jwt['email'])
            if user:
                return redirect("Quiz/inicialize/{}".format(decode_jwt['email']))
            else:
                Player.objects.create(email=decode_jwt['email'])
                return redirect("Quiz/inicialize/{}".format(decode_jwt['email']))
        else:
            return render(request, "Users/login_page.html")
    else:
        return redirect('main-game-page')