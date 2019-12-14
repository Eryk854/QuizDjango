import jwt
from django.http import request
from user.models import Player,Account

from .models import Account

# def index(request):
#     from Pytania.views import flaga
#     print(flaga)
#     if not flaga:
#         token = request.GET.get('token')
#         print(token)
#         if token:
#             decode_jwt = jwt.decode(token, '926D96C90030DD58429D2751AC1BDBBC', algorithms='HS512',verify = False)
#             user = Player.objects.filter(email=decode_jwt['email'])
#             if user:
#                 return redirect("Quiz/inicialize/{}".format(decode_jwt['email']))
#             else:
#                 Player.objects.create(email=decode_jwt['email'])
#                 return redirect("Quiz/inicialize/{}".format(decode_jwt['email']))
#         else:
#             return render(request, "Users/login_page.html")
#     else:
#         return redirect('main-game-page')
class SocialBackend(object):
    def authenticate(self, request, **kwargs):
        token = request.GET.get('token')
        print(token)
        if token:
            decode_jwt = jwt.decode(token, '926D96C90030DD58429D2751AC1BDBBC', algorithms='HS512',verify = False)
            print(decode_jwt['email'])
            user = Account.objects.filter(email=decode_jwt['email'])
            if user:
                 #user istnieje
                 return Account.objects.get(email=decode_jwt['email'])
            else:
                #tworzymy usera
                Account.objects.create_user(decode_jwt['email'],'test')
                return Account.objects.get(email=decode_jwt['email'])

        return None

    def get_user(self,user_id):
        try:
           return Account.objects.get(pk=user_id)
        except Account.DoesNotExist:
            return None