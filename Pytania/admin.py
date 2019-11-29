from django.contrib import admin
from .models import Pytanie
# Register your models here.


class Pytanie_admin(admin.ModelAdmin):
    list_display = ('id','tresc')

admin.site.register(Pytanie,Pytanie_admin)
