from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from  .models import Pytanie
from django.contrib.auth.decorators import login_required
from user.models import Player, Account
from questionApi.models import SuggestQuestion
from random import randint
from django.core import serializers
from django.views.generic.edit import FormView, CreateView
from .forms import NewQuestionForm
import requests
from django.core import serializers
from rest_framework.authtoken.models import Token
# Create your views here.


@login_required
def index(request):
    if not Token.objects.filter(user_id=request.user.id):
        token = Token.objects.create(user=request.user)
        print(token)
    wynik = Player.objects.get(email=request.user.email).best_score
    return render(request, "Pytania/index.html",
                    {'player': request.user.email,
                     'score': wynik})


def get_questions():
    count = Pytanie.objects.count()
    questions = []
    while len(questions) < 5:
        random_object = Pytanie.objects.all()[randint(0, count - 1)]
        while random_object in questions:
            random_object = Pytanie.objects.all()[randint(0, count - 1)]
        questions.append(random_object)
    questions = serializers.serialize('json', questions)
    return questions


def get_questions_from_api(request):

    token = 'b5a4ff878af1ccfee6b08a08a28be22c0ac7cce9'
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
    print(request.session['nr_pytania'])
    actual_question = request.session['pytania'][request.session['nr_pytania']]

    print(actual_question)
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
        player = Player.objects.get(email=self.request.user)
        initial['player'] = player
        return initial

    # def form_valid(self, form):
    #     print(type(self.request.user))
    #     cleaned_data = form.cleaned_data
    #     player = Player.objects.get(email=self.request.user)
    #     cleaned_data['player'] = player
    #     new_question = SugestQuestion.objects.create(cleaned_data)
    #     #new_question.save()
    #     print(cleaned_data)
