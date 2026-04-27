import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

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
    return MinecraftVersion.objects.create(
        version_number="1.21",
        release_date=date(2024, 6, 13),
        is_latest=True
    )

@pytest.fixture
def test_item(test_version):
    from items.models import Item
    item = Item.objects.create(
        item_id="minecraft:oak_planks",
        name="Дубовые доски",
        name_en="Oak Planks",
        category="block",
        stack_size=64,
        rarity="common"
    )
    item.versions.add(test_version)
    return item

@pytest.fixture
def test_mob(test_version):
    from mobs.models import Mob
    mob = Mob.objects.create(
        mob_id="minecraft:zombie",
        name="Zombie",
        health=20.0,
        damage=3.0,
        behavior="hostile",
        category="monster",
        experience=5,
        description="Враждебный моб"
    )
    mob.versions.add(test_version)
    return mob