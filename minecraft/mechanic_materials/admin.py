from django.contrib import admin
from .models import MechanicMaterial

@admin.register(MechanicMaterial)
class MechanicMaterialAdmin(admin.ModelAdmin):
    list_display = ['mechanic', 'item', 'count', 'is_consumable']
    list_filter = ['is_consumable', 'mechanic__category']
    search_fields = ['mechanic__title', 'item__name']