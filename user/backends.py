import jwt
from django.http import request
from user.models import Player,Account
from django.contrib import messages

from .models import Account

class SocialBackend(object):
    def authenticate(self, request, **kwargs):
        token = request.GET.get('token')
        if token:
            decode_jwt = jwt.decode(token, '926D96C90030DD58429D2751AC1BDBBC', algorithms='HS512',verify = False)
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