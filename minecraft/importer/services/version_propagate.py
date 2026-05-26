from django.db import transaction

from items.models import Item
from loot_drops.models import LootDrop
from mobs.models import Mob
from recipes.models import Recipe
from structures.models import Structure
from versions.models import MinecraftVersion


def _versions_from_intro(intro_version: str | None, versions_ordered: list[MinecraftVersion]) -> list[MinecraftVersion]:
    if not intro_version:
        return list(versions_ordered)
    intro = MinecraftVersion.objects.filter(version_number=intro_version).first()
    if not intro:
        return list(versions_ordered)
    return [v for v in versions_ordered if v.release_date >= intro.release_date]


@transaction.atomic
def propagate_versions(
    mob_intro: dict[str, str] | None = None,
    structure_intro: dict[str, str] | None = None,
) -> dict[str, int]:
    """Кумулятивно привязать контент ко всем версиям >= версии появления."""
    mob_intro = mob_intro or {}
    structure_intro = structure_intro or {}
    versions_ordered = list(MinecraftVersion.objects.order_by('release_date'))
    counts = {
        'items': 0,
        'mobs': 0,
        'structures': 0,
        'recipes': 0,
        'loot_drops': 0,
    }

    for item in Item.objects.select_related('added_in_version').iterator():
        intro = item.added_in_version.version_number if item.added_in_version else None
        target = _versions_from_intro(intro, versions_ordered)
        item.versions.set(target)
        counts['items'] += 1

    for mob in Mob.objects.iterator():
        intro = mob_intro.get(mob.mob_id)
        target = _versions_from_intro(intro, versions_ordered)
        mob.versions.set(target)
        counts['mobs'] += 1

    for structure in Structure.objects.iterator():
        intro = structure_intro.get(structure.structure_id)
        target = _versions_from_intro(intro, versions_ordered)
        structure.versions.set(target)
        counts['structures'] += 1

    for recipe in Recipe.objects.select_related('result_item', 'result_item__added_in_version').iterator():
        intro = None
        if recipe.result_item.added_in_version:
            intro = recipe.result_item.added_in_version.version_number
        target = _versions_from_intro(intro, versions_ordered)
        recipe.versions.set(target)
        counts['recipes'] += 1

    for drop in LootDrop.objects.select_related('mob').iterator():
        intro = mob_intro.get(drop.mob.mob_id)
        target = _versions_from_intro(intro, versions_ordered)
        drop.versions.set(target)
        counts['loot_drops'] += 1

    return counts
