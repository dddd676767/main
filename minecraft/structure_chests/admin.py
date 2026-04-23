from django.contrib import admin
from .models import StructureChest

@admin.register(StructureChest)
class StructureChestAdmin(admin.ModelAdmin):
    list_display = ['name', 'structure', 'average_value']
    list_filter = ['structure__rarity']
    search_fields = ['name', 'structure__name']