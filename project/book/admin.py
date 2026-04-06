from django.contrib import admin
from .models import *

# Базовые модели
@admin.register(MinecraftVersion)
class MinecraftVersionAdmin(admin.ModelAdmin):
    list_display = ['version_number', 'release_date', 'is_latest']
    list_filter = ['is_latest']
    search_fields = ['version_number']

@admin.register(Dimension)
class DimensionAdmin(admin.ModelAdmin):
    list_display = ['name_ru', 'name']
    search_fields = ['name_ru', 'name']

@admin.register(Biome)
class BiomeAdmin(admin.ModelAdmin):
    list_display = ['name_ru', 'dimension', 'temperature']
    list_filter = ['dimension']
    search_fields = ['name_ru', 'name']

# Предметы и рецепты
@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'rarity', 'stack_size']
    list_filter = ['category', 'rarity', 'versions']
    search_fields = ['name', 'name_en', 'item_id']
    filter_horizontal = ['versions']

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['result_item', 'result_count', 'recipe_type']
    list_filter = ['recipe_type', 'versions']
    search_fields = ['result_item__name']
    filter_horizontal = ['versions']

class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1

@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ['recipe', 'item', 'count', 'position_row', 'position_col']
    list_filter = ['recipe__recipe_type']

# Мобы
@admin.register(Mob)
class MobAdmin(admin.ModelAdmin):
    list_display = ['name', 'behavior', 'category', 'health', 'damage']
    list_filter = ['behavior', 'category', 'spawns_in', 'versions']
    search_fields = ['name', 'name_en', 'mob_id']
    filter_horizontal = ['spawns_in', 'biomes', 'versions']

class LootDropInline(admin.TabularInline):
    model = LootDrop
    extra = 1

@admin.register(LootDrop)
class LootDropAdmin(admin.ModelAdmin):
    list_display = ['mob', 'item', 'chance', 'min_count', 'max_count', 'is_rare']
    list_filter = ['is_rare', 'versions']

@admin.register(MobSpawnCondition)
class MobSpawnConditionAdmin(admin.ModelAdmin):
    list_display = ['mob', 'dimension', 'biome', 'light_level_max', 'only_at_night']
    list_filter = ['dimension', 'only_at_night']

# Структуры
@admin.register(Structure)
class StructureAdmin(admin.ModelAdmin):
    list_display = ['name', 'rarity']
    list_filter = ['rarity', 'dimensions', 'versions']
    search_fields = ['name', 'name_en', 'structure_id']
    filter_horizontal = ['dimensions', 'biomes', 'versions']

class ChestLootItemInline(admin.TabularInline):
    model = ChestLootItem
    extra = 1

@admin.register(StructureChest)
class StructureChestAdmin(admin.ModelAdmin):
    list_display = ['name', 'structure', 'average_value']
    list_filter = ['structure__rarity']
    inlines = [ChestLootItemInline]

# Механики
@admin.register(Mechanic)
class MechanicAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'difficulty', 'estimated_time']
    list_filter = ['category', 'difficulty', 'versions']
    search_fields = ['title', 'title_en', 'mechanic_id']
    filter_horizontal = ['versions']

class MechanicStepInline(admin.TabularInline):
    model = MechanicStep
    extra = 1

class MechanicMaterialInline(admin.TabularInline):
    model = MechanicMaterial
    extra = 1

@admin.register(MechanicStep)
class MechanicStepAdmin(admin.ModelAdmin):
    list_display = ['mechanic', 'step_number', 'title']
    list_filter = ['mechanic__category']

@admin.register(MechanicMaterial)
class MechanicMaterialAdmin(admin.ModelAdmin):
    list_display = ['mechanic', 'item', 'count', 'is_consumable']

# Пользовательские данные
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'selected_version', 'dark_mode', 'language', 'last_visited']
    list_filter = ['dark_mode', 'language', 'selected_version']
    search_fields = ['user_id']

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'type', 'item_id', 'added_at']
    list_filter = ['type', 'added_at']
    search_fields = ['user__user_id', 'item_id']

@admin.register(SearchHistory)
class SearchHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'query', 'timestamp']
    list_filter = ['timestamp']
    search_fields = ['user__user_id', 'query']

@admin.register(CompletedTutorial)
class CompletedTutorialAdmin(admin.ModelAdmin):
    list_display = ['user', 'mechanic', 'completed_at']
    list_filter = ['completed_at']
    search_fields = ['user__user_id', 'mechanic__title']