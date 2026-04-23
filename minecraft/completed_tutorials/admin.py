from django.contrib import admin
from .models import CompletedTutorial

@admin.register(CompletedTutorial)
class CompletedTutorialAdmin(admin.ModelAdmin):
    list_display = ['user', 'mechanic', 'completed_at']
    list_filter = ['completed_at']
    search_fields = ['user__user_id', 'mechanic__title']