import os
import sys
import django


sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from versions.services import VersionService
from items.services import ItemService
from mobs.services import MobService
from favorites.services import FavoriteService

latest = VersionService.get_latest()
print(f"Последняя версия: {latest}")

items = ItemService.get_all()
print(f"Количество предметов: {items.count()}")

diamond = ItemService.search("diamond")
print(f"Поиск 'Алмаза': {diamond.count()}")

mobs = MobService.get_all()
print(f"Количество мобов: {mobs.count()}")

fav = FavoriteService.add("test_user", "minecraft:diamond", "item")
print(f"Добавлено в избранное: {fav}")

print("=" * 50)