from django.contrib import admin
from .models import RecipeIngredient

@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ['recipe', 'item', 'count', 'position_row', 'position_col']
    list_filter = ['recipe__recipe_type']
    search_fields = ['recipe__result_item__name', 'item__name']