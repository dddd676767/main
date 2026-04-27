import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def admin_user():
    user = User.objects.create_superuser(
        username='admin',
        email='admin@test.com',
        password='admin123'
    )
    return user

@pytest.fixture
def admin_client(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    return api_client

@pytest.fixture
def test_version():
    from versions.models import MinecraftVersion
    from datetime import date
    version, created = MinecraftVersion.objects.get_or_create(
        version_number="1.21",
        defaults={
            'release_date': date(2024, 6, 13),
            'is_latest': True
        }
    )
    return version

@pytest.fixture
def test_dimension():
    from dimensions.models import Dimension
    dimension, created = Dimension.objects.get_or_create(
        name="Overworld",
        defaults={'name_ru': "Верхний мир"}
    )
    return dimension

@pytest.fixture
def test_item(test_version):
    from items.models import Item
    item, created = Item.objects.get_or_create(
        item_id="minecraft:oak_planks",
        defaults={
            'name': "Дубовые доски",
            'name_en': "Oak Planks",
            'category': "block",
            'stack_size': 64,
            'rarity': "common"
        }
    )
    if created:
        item.versions.add(test_version)
    return item

@pytest.fixture
def test_mob(test_version, test_dimension):
    from mobs.models import Mob
    from biomes.models import Biome
    
    biome, _ = Biome.objects.get_or_create(
        name="Plains",
        defaults={
            'name_ru': "Равнины",
            'dimension': test_dimension,
            'temperature': 0.8
        }
    )
    
    mob, created = Mob.objects.get_or_create(
        mob_id="minecraft:zombie",
        defaults={
            'name': "Zombie",
            'name_en': "Zombie",
            'health': 20.0,
            'damage': 3.0,
            'behavior': "hostile",
            'category': "monster",
            'experience': 5,
            'description': "Враждебный моб"
        }
    )
    if created:
        mob.versions.add(test_version)
        mob.spawns_in.add(test_dimension)
        mob.biomes.add(biome)
    return mob