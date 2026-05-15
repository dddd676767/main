"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from versions.views import MinecraftVersionViewSet
from dimensions.views import DimensionViewSet
from biomes.views import BiomeViewSet
from minecraft.items.api.views import ItemViewSet
from recipes.views import RecipeViewSet
from recipe_ingredients.views import RecipeIngredientViewSet
from minecraft.mobs.api.views import MobViewSet
from minecraft.loot_drops.api.views import LootDropViewSet
from minecraft.mob_spawns.api.views import MobSpawnConditionViewSet
from structures.views import StructureViewSet
from structure_chests.views import StructureChestViewSet
from chest_loots.views import ChestLootItemViewSet
from minecraft.mechanics.api.views import MechanicViewSet
from minecraft.mechanic_steps.api.views import MechanicStepViewSet
from minecraft.mechanic_materials.api.views import MechanicMaterialViewSet
from user_profiles.views import UserProfileViewSet
from minecraft.favorites.api.views import FavoriteViewSet
from search_history.views import SearchHistoryViewSet
from completed_tutorials.views import CompletedTutorialViewSet

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

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]