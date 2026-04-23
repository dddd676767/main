from django.contrib import admin
from .models import MobSpawnCondition

@admin.register(MobSpawnCondition)
class MobSpawnConditionAdmin(admin.ModelAdmin):
    list_display = ['mob', 'dimension', 'biome', 'light_level_max', 'only_at_night']
    list_filter = ['dimension', 'only_at_night']
    search_fields = ['mob__name']