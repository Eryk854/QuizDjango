from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from  .models import Pytanie
from django.contrib.auth.decorators import login_required
from user.models import Player,Account
from random import randint
from django.core import serializers
# Create your views here.


@login_required
def index(request):
    wynik = Player.objects.get(email=request.user.email).best_score
    return render(request, "Pytania/index.html",
                    {'player': request.user.email,
                     'score': wynik})


def get_questions():
    count = Pytanie.objects.count()
    questions = []
    while len(questions)<5:
        random_object = Pytanie.objects.all()[randint(0, count - 1)]
        while random_object in questions:
            random_object = Pytanie.objects.all()[randint(0, count - 1)]
        questions.append(random_object)
    questions = serializers.serialize('json',questions)
    return questions

@login_required
def pierwsze_pytanie(request):
    request.session['bledne_odpowiedzi'] = []
    request.session['moje_bledne'] = []
    request.session['nr_pytania'] = 0
    request.session['poprawne_odpowiedzi'] = 0
    request.session['pytania'] = get_questions()
    request.session.modified = True
    return redirect('/Quiz/questions/')

@login_required
def questions(request):
    if request.session['pytania']:
        # pytania istnieją czas na nie odpowiedzieć
        i = 0
        for obj in serializers.deserialize('json', request.session['pytania']):
            if request.session['nr_pytania']==i:
                return render(request, "Pytania/pytanie.html",
                              {'pytanie':obj.object,
                                'nr_pytania':request.session['nr_pytania']+1,
                                'player':request.user.email})
            i+=1

@csrf_exempt
def sprawdz_odp(request, pytanie_id):
    odp = request.POST['options']
    true_odp = Pytanie.objects.get(id=pytanie_id)
    true_odp = true_odp.poprawnaOdp
    if odp == true_odp:
        request.session['poprawne_odpowiedzi'] += 1
    else:
        request.session['bledne_odpowiedzi'].append(pytanie_id)
        request.session['moje_bledne'].append(odp)

    request.session['nr_pytania']+=1

    if request.session['nr_pytania'] == 5:
        return redirect('end_quiz')
    else:
        return HttpResponseRedirect('/Quiz/questions/')


@login_required
def zakoncz_quiz(request):
    bledne_odpowiedzi = request.session['bledne_odpowiedzi']
    moje_bledne = request.session['moje_bledne']
    i = 0
    klasy = []
    pytania = []

    user = Player.objects.get(email=request.user.email)
    wynik = user.best_score
    if request.session['poprawne_odpowiedzi'] > wynik:
        user.best_score = request.session['poprawne_odpowiedzi']
        user.save()

    for nr_pytania in bledne_odpowiedzi:
        slownik = dict()
        pytanie = Pytanie.objects.get(id=nr_pytania)

        litery = ["A","B","C","D"]
        litery.remove(pytanie.poprawnaOdp)

        slownik['odp'+pytanie.poprawnaOdp] = "btn btn-success btn-lg btn-block"
        if moje_bledne[i]!='E':
            slownik['odp'+moje_bledne[i]] = "btn btn-danger btn-lg btn-block"
            litery.remove((moje_bledne[i]))
        for litera in litery:
            slownik['odp'+litera] = 'btn btn-info btn-lg btn-block'
        i+=1
        klasy.append(slownik)
        pytania.append(pytanie)

    my_elements = zip(klasy, pytania)
    return render(request,"Pytania/koniec.html",
                  {'my_elements':my_elements,
                   'poprawne_odp': request.session['poprawne_odpowiedzi'],
                   'player':request.user.email})
