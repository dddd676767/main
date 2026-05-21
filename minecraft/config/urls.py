# config/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from versions.api.views import MinecraftVersionViewSet
from dimensions.api.views import DimensionViewSet
from biomes.api.views import BiomeViewSet
from items.api.views import ItemViewSet
from recipes.api.views import RecipeViewSet
from recipe_ingredients.api.views import RecipeIngredientViewSet
from mobs.api.views import MobViewSet
from loot_drops.api.views import LootDropViewSet
from mob_spawns.api.views import MobSpawnConditionViewSet
from structures.api.views import StructureViewSet
from structure_chests.api.views import StructureChestViewSet
from chest_loots.api.views import ChestLootItemViewSet
from mechanics.api.views import MechanicViewSet
from mechanic_steps.api.views import MechanicStepViewSet
from mechanic_materials.api.views import MechanicMaterialViewSet
from user_profiles.api.views import UserProfileViewSet
from favorites.api.views import FavoriteViewSet
from search_history.api.views import SearchHistoryViewSet
from completed_tutorials.api.views import CompletedTutorialViewSet
from effects.api.views import EffectViewSet
from enchantments.api.views import EnchantmentViewSet

router = DefaultRouter()
router.register(r'versions', MinecraftVersionViewSet)
router.register(r'dimensions', DimensionViewSet)
router.register(r'biomes', BiomeViewSet)
router.register(r'items', ItemViewSet)
router.register(r'recipes', RecipeViewSet)
router.register(r'recipe-ingredients', RecipeIngredientViewSet)
router.register(r'mobs', MobViewSet)
router.register(r'loot-drops', LootDropViewSet)
router.register(r'mob-spawns', MobSpawnConditionViewSet)
router.register(r'structures', StructureViewSet)
router.register(r'structure-chests', StructureChestViewSet)
router.register(r'chest-loots', ChestLootItemViewSet)
router.register(r'mechanics', MechanicViewSet)
router.register(r'mechanic-steps', MechanicStepViewSet)
router.register(r'mechanic-materials', MechanicMaterialViewSet)
router.register(r'user-profiles', UserProfileViewSet)
router.register(r'favorites', FavoriteViewSet)
router.register(r'search-history', SearchHistoryViewSet)
router.register(r'completed-tutorials', CompletedTutorialViewSet)
router.register(r'effects', EffectViewSet)
router.register(r'enchantments', EnchantmentViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]