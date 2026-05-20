from datetime import date

import pytest
from django.test import TestCase

from items.models import Item
from importer.services.version_propagate import propagate_versions
from versions.models import MinecraftVersion


@pytest.mark.django_db
class TestVersionPropagate(TestCase):
    def setUp(self):
        self.v10 = MinecraftVersion.objects.create(
            version_number='1.0.0',
            release_date=date(2011, 11, 18),
        )
        self.v16 = MinecraftVersion.objects.create(
            version_number='1.16',
            release_date=date(2020, 6, 23),
        )
        self.v21 = MinecraftVersion.objects.create(
            version_number='1.21',
            release_date=date(2024, 6, 13),
            is_latest=True,
        )
        self.old_item = Item.objects.create(
            item_id='minecraft:dirt',
            name='Земля',
            name_en='Dirt',
            category='block',
            added_in_version=self.v10,
        )
        self.new_item = Item.objects.create(
            item_id='minecraft:breeze_rod',
            name='Стержень',
            name_en='Breeze Rod',
            category='material',
            added_in_version=self.v21,
        )

    def test_cumulative_item_versions(self):
        propagate_versions()
        self.old_item.refresh_from_db()
        self.new_item.refresh_from_db()
        self.assertEqual(self.old_item.versions.count(), 3)
        self.assertEqual(self.new_item.versions.count(), 1)
        self.assertTrue(self.old_item.versions.filter(version_number='1.16').exists())
        self.assertFalse(self.new_item.versions.filter(version_number='1.16').exists())
