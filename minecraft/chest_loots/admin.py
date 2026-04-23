from django.contrib import admin
from .models import ChestLootItem

@admin.register(ChestLootItem)
class ChestLootItemAdmin(admin.ModelAdmin):
    list_display = ['chest', 'item', 'chance', 'min_count', 'max_count']
    list_filter = ['chest__structure']
    search_fields = ['chest__name', 'item__name']