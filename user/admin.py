from django.contrib import admin
from .models import Player, Account
from questionApi.models import Question, SuggestQuestion
# Register your models here.


class Players_admin(admin.ModelAdmin):
    list_display = ('email', 'best_score')

admin.site.register(Player,Players_admin)
admin.site.register(Account)
admin.site.register(Question)
admin.site.register(SuggestQuestion)

