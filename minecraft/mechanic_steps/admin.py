from django.contrib import admin
from .models import MechanicStep

@admin.register(MechanicStep)
class MechanicStepAdmin(admin.ModelAdmin):
    list_display = ['mechanic', 'step_number', 'title']
    list_filter = ['mechanic__category']
    search_fields = ['title', 'mechanic__title']
    ordering = ['mechanic', 'step_number']