from django.contrib import admin
from .models import SearchHistory

@admin.register(SearchHistory)
class SearchHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'query', 'timestamp']
    list_filter = ['timestamp']
    search_fields = ['user__user_id', 'query']