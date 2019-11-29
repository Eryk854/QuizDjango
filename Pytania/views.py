from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from  .models import Pytanie
from user.models import Player
from random import randint
# Create your views here.

nr_pytania = 0
poprawne_odpowiedzi = 0
lista_pytan = []
bledne_odpowiedzi = []
moje_bledne =[]
user_email = ''
def get_random_element():
    global lista_pytan
    count = Pytanie.objects.count()
    random_object = Pytanie.objects.all()[randint(0, count - 1)]
    while random_object.id in lista_pytan:
        random_object = Pytanie.objects.all()[randint(0,count-1)]
    return random_object


def pierwsze_pytanie(request):
    global nr_pytania, poprawne_odpowiedzi,lista_pytan,bledne_odpowiedzi,moje_bledne
    global user_email
    nr_pytania = 0
    poprawne_odpowiedzi = 0
    lista_pytan = []
    bledne_odpowiedzi = []
    moje_bledne = []
    pytanie = get_random_element()
    return render(request,"Pytania/pytanie.html",
                  {'pytanie':pytanie,
                   'nr_pytania':nr_pytania+1,
                  'player':user_email})

def inicialize_user(request,email):
    global user_email
    user_email = email
    return redirect("../")

def index(request):
    global user_email
    user = Player.objects.get(email=user_email)
    wynik = user.best_score
    return render(request, "Pytania/index.html",
                  {'player':user_email,
                   'score':wynik})

@csrf_exempt
def sprawdz_odp(request,pytanie_id):
    global poprawne_odpowiedzi,nr_pytania,lista_pytan
    odp = request.POST['options']
    true_odp = Pytanie.objects.get(id=pytanie_id)
    true_odp = true_odp.poprawnaOdp
    if odp == true_odp:
        poprawne_odpowiedzi+=1
    else:
        global bledne_odpowiedzi,moje_bledne
        bledne_odpowiedzi.append(pytanie_id)
        moje_bledne.append(odp)

    nr_pytania+=1
    lista_pytan.append(pytanie_id)

    if nr_pytania == 5:
        return HttpResponseRedirect('../../Quiz/zakoncz_quiz')
    else:
        return HttpResponseRedirect('../../Quiz/kolejne_pytanie')


def kolejne_pytanie(request):
    global nr_pytania
    global user_email
    pytanie = get_random_element()
    return render(request, "Pytania/pytanie.html",
                  {'pytanie': pytanie,
                   'nr_pytania':nr_pytania+1,
                   'player':user_email})


def zakoncz_quiz(request):
    global bledne_odpowiedzi,moje_bledne,poprawne_odpowiedzi
    global user_email
    i = 0
    klasy = []
    pytania = []

    user = Player.objects.get(email=user_email)
    wynik = user.best_score
    if poprawne_odpowiedzi > wynik:
        user.best_score = poprawne_odpowiedzi
        user.save()

    for nr_pytania in bledne_odpowiedzi:
        slownik = dict()
        pytanie = Pytanie.objects.get(id=nr_pytania)
        """slownik['odpA'] = "btn btn-succes btn-sm" if pytanie.poprawnaOdp == 'A' else "btn btn-info btn-lg btn-block"
        slownik['odpB'] = "btn btn-succes btn-sm" if pytanie.poprawnaOdp == 'B' else "btn btn-info btn-lg btn-block"
        slownik['odpC'] = "btn btn-succes btn-sm" if pytanie.poprawnaOdp == 'C' else "btn btn-info btn-lg btn-block"
        slownik['odpD'] = "btn btn-succes btn-sm" if pytanie.poprawnaOdp == 'D' else "btn btn-info btn-lg btn-block"

        slownik['odpA'] = "btn btn-danger btn-sm" if moje_bledne[i] == 'A' else "btn btn-info btn-lg btn-block"
        slownik['odpB'] = "btn btn-danger btn-sm" if moje_bledne[i] == 'B' else "btn btn-info btn-lg btn-block"
        slownik['odpC'] = "btn btn-danger btn-sm" if moje_bledne[i] == 'C' else "btn btn-info btn-lg btn-block"
        slownik['odpD'] = "btn btn-danger btn-sm" if moje_bledne[i] == 'D' else "btn btn-info btn-lg btn-block"""

        litery = ["A","B","C","D"]
        litery.remove(pytanie.poprawnaOdp)
        litery.remove((moje_bledne[i]))
        slownik['odp'+pytanie.poprawnaOdp] = "btn btn-success btn-lg btn-block"
        slownik['odp'+moje_bledne[i]] = "btn btn-danger btn-lg btn-block"
        for litera in litery:
            slownik['odp'+litera] = 'btn btn-info btn-lg btn-block'
        i+=1
        klasy.append(slownik)
        pytania.append(pytanie)

    my_html = ''
    for i in range(len(klasy)):
        my_html += "<h5>"+pytania[i].tresc+"</h5>"
        my_html +="<button type='button' class='"+klasy[i]['odpA']+"' disabled>"+pytania[i].odpA+"</button> \n"
        my_html += "<button type='button' class='" + klasy[i]['odpB'] + "' disabled>" + pytania[i].odpB + "</button> \n"
        my_html += "<button type='button' class='" + klasy[i]['odpC'] + "' disabled>" + pytania[i].odpC + "</button> \n"
        my_html += "<button type='button' class='" + klasy[i]['odpD'] + "' disabled>" + pytania[i].odpD + "</button> \n"

    return render(request,"Pytania/koniec.html",
                  {"klasy":klasy,
                   "pytanie":pytania,
                   'range':range(len(klasy)),
                   "my_html":my_html,
                   'poprawne_odp': poprawne_odpowiedzi,
                   'player':user_email})