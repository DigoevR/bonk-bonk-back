from django.contrib import admin

from tennis.models import Game, Match

admin.site.register((Match, Game))
