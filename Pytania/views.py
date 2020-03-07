from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.views.generic.edit import FormView, CreateView
from django.views.generic.list import ListView
from django.core.paginator import Paginator

from rest_framework.authtoken.models import Token

from user.models import Player, Account
from questionApi.models import SuggestQuestion
from .forms import NewQuestionForm
from secret_settings import *

from random import randint
import requests


@login_required
def index(request):
    if not Token.objects.filter(user_id=request.user.id):
        token = Token.objects.create(user=request.user)
        print(token)
    wynik = Player.objects.get(email=request.user.email).best_score
    return render(request, "Pytania/index.html",
                    {'player': request.user.email,
                     'score': wynik})


def get_questions_from_api(request):

    token = API_KEY
    headers = {'Authorization': 'Token {}'.format(token)}
    api_questions = requests.get("http://localhost:8000/api/question/", headers=headers).json()
    count = len(api_questions)
    questions = []
    while len(questions) < 5:
        random_object = api_questions[randint(0, count - 1)]
        while random_object in questions:
            random_object = api_questions[randint(0, count - 1)]
        questions.append(random_object)
    return questions


@login_required
def pierwsze_pytanie(request):
    request.session['bledne_odpowiedzi'] = []
    request.session['moje_bledne'] = []
    request.session['nr_pytania'] = 0
    request.session['poprawne_odpowiedzi'] = 0
    request.session['pytania'] = get_questions_from_api(request)
    request.session.modified = True
    return redirect('/Quiz/questions/')

@login_required
def questions(request):
    if request.session['pytania']:
        # pytania istnieją czas na nie odpowiedzieć
        i = 0
        for obj in request.session['pytania']:
            if request.session['nr_pytania'] == i:
                return render(request, "Pytania/pytanie.html",
                              {'pytanie': obj,
                               'nr_pytania': request.session['nr_pytania']+1,
                               'player': request.user.email})
            i += 1

@csrf_exempt
def sprawdz_odp(request):
    odp = request.POST['options']
    actual_question = request.session['pytania'][request.session['nr_pytania']]

    true_odp = actual_question['correct_answer']
    if odp == true_odp:
        request.session['poprawne_odpowiedzi'] += 1
    else:
        request.session['bledne_odpowiedzi'].append(actual_question)
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

    for pytanie in bledne_odpowiedzi:
        slownik = dict()
        litery = ["A", "B", "C", "D"]
        litery.remove(pytanie['correct_answer'])
        print(moje_bledne)
        slownik['answer'+pytanie['correct_answer']] = "btn btn-success btn-lg btn-block"
        if moje_bledne[i]!='E':
            slownik['answer'+moje_bledne[i]] = "btn btn-danger btn-lg btn-block"
            litery.remove((moje_bledne[i]))
        for litera in litery:
            slownik['answer'+litera] = 'btn btn-info btn-lg btn-block'
        i += 1
        klasy.append(slownik)
        pytania.append(pytanie)

    my_elements = zip(klasy, pytania)
    return render(request,"Pytania/koniec.html",
                  {'my_elements':my_elements,
                   'poprawne_odp': request.session['poprawne_odpowiedzi'],
                   'player':request.user.email})


class AddNewQuestionView(CreateView):
    form_class = NewQuestionForm
    template_name = "Pytania/new_question_form.html"
    success_url = "/Quiz/"

    def get_initial(self, *args, **kwargs):
        initial = super(AddNewQuestionView, self).get_initial(**kwargs)
        player = Account.objects.get(email=self.request.user)
        print(player)
        initial['player'] = player
        print(initial)
        return initial

class QuestionList(ListView):
    template_name = "Pytania/question_list.html"
    model = SuggestQuestion

    def get_context_data(self, **kwargs):
        token = Token.objects.get(user=self.request.user)
        context = super().get_context_data(**kwargs)
        headers = {'Authorization': 'Token {}'.format(token)}
        r = requests.get("http://localhost:8000/api/question/", headers=headers)
        questions = r.json()

        paginator = Paginator(questions, 5)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['page_obj'] = page_obj
        return context

    # def get_queryset(self):
    #     return True
