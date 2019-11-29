from django.contrib import admin
from .models import Player
# Register your models here.


class Players_admin(admin.ModelAdmin):
    list_display = ('email','best_score')

admin.site.register(Player,Players_admin)
