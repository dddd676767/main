# test_services.py
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

print("=" * 50)
print("ПРОВЕРКА СЕРВИСОВ")
print("=" * 50)

# 1. Проверка VersionService
print("\n1. VersionService:")
from versions.services import VersionService
current = VersionService.get_current_version()
print(f"   ✅ Текущая версия: {current}")

# 2. Проверка DimensionService
print("\n2. DimensionService:")
from dimensions.services import DimensionService
dims = DimensionService.get_all_dimensions()
print(f"   ✅ Измерений в БД: {len(dims)}")

# 3. Проверка BiomeService
print("\n3. BiomeService:")
from biomes.services import BiomeService
biomes = BiomeService.get_all_biomes()
print(f"   ✅ Биомов в БД: {len(biomes)}")

# 4. Проверка ItemService
print("\n4. ItemService:")
from items.services import ItemService
items = ItemService.search_items("алмаз")
print(f"   ✅ Найдено предметов по запросу 'алмаз': {len(items)}")

# 5. Проверка MobService
print("\n5. MobService:")
from mobs.services import MobService
mobs = MobService.search_mobs("зомби")
print(f"   ✅ Найдено мобов по запросу 'зомби': {len(mobs)}")

# 6. Проверка RecipeService
print("\n6. RecipeService:")
from recipes.services import RecipeService
recipes = RecipeService.get_recipes_by_type("crafting_3x3")
print(f"   ✅ Рецептов типа crafting_3x3: {len(recipes)}")

# 7. Проверка FavoriteService
print("\n7. FavoriteService:")
from favorites.services import FavoriteService
result = FavoriteService.add_to_favorites("test_user", "minecraft:diamond", "item")
print(f"   ✅ Добавление в избранное: {'создано' if result else 'уже существует'}")

print("\n" + "=" * 50)
print("✅ ВСЕ СЕРВИСЫ РАБОТАЮТ!")
print("=" * 50)