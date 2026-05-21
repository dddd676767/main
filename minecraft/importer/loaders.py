from dataclasses import dataclass, field
from datetime import date

from django.db import transaction

from biomes.models import Biome
from dimensions.models import Dimension
from effects.models import Effect
from enchantments.models import Enchantment
from importer.client import WikiClient
from importer.mappers import category_from_group_slug, dimension_for_biome, normalize_item_id
from importer.parsers import (
    parse_biomes_page,
    parse_effects_page,
    parse_enchantments_page,
    parse_group_page,
    parse_item_detail,
    parse_item_recipes,
    parse_mob_detail,
    parse_mobs_list_page,
    parse_structures_from_locate,
)
from importer.parsers.html import slug_from_url
from importer.wp_api import iter_posts
from items.models import Item
from loot_drops.models import LootDrop
from mob_spawns.models import MobSpawnCondition
from mobs.models import Mob
from recipe_ingredients.models import RecipeIngredient
from recipes.models import Recipe
from structures.models import Structure
from versions.models import MinecraftVersion

PREDMET_CATEGORY = 3
GROUP_CATEGORY = 9
MOB_CATEGORY = 7


@dataclass
class ImportStats:
    created: int = 0
    updated: int = 0
    skipped: int = 0
    errors: list[str] = field(default_factory=list)

    def merge(self, other: 'ImportStats'):
        self.created += other.created
        self.updated += other.updated
        self.skipped += other.skipped
        self.errors.extend(other.errors)


class WikiImporter:
    def __init__(self, client: WikiClient, dry_run: bool = False, deep: bool = False):
        self.client = client
        self.dry_run = dry_run
        self.deep = deep
        self.dimensions: dict[str, Dimension] = {}
        self.version: MinecraftVersion | None = None
        self.item_by_name: dict[str, Item] = {}

    def seed(self) -> ImportStats:
        stats = ImportStats()
        dims = [
            ('Overworld', 'Верхний мир'),
            ('Nether', 'Нижний мир'),
            ('End', 'Край'),
        ]
        for name, name_ru in dims:
            if self.dry_run:
                stats.created += 1
                continue
            obj, created = Dimension.objects.get_or_create(
                name=name, defaults={'name_ru': name_ru},
            )
            self.dimensions[name] = obj
            stats.created += created
            stats.updated += not created

        if self.dry_run:
            stats.created += 1
            return stats

        self.version, created = MinecraftVersion.objects.get_or_create(
            version_number='1.21',
            defaults={'release_date': date(2024, 6, 13), 'is_latest': True},
        )
        MinecraftVersion.objects.exclude(pk=self.version.pk).update(is_latest=False)
        stats.created += created
        stats.updated += not created
        return stats

    def import_biomes(self) -> ImportStats:
        stats = ImportStats()
        html = self.client.fetch('biomy/')
        for data in parse_biomes_page(html):
            dim = self.dimensions.get(data['dimension'])
            if not dim and not self.dry_run:
                stats.errors.append(f"No dimension {data['dimension']}")
                stats.skipped += 1
                continue
            if self.dry_run:
                stats.created += 1
                continue
            _, created = Biome.objects.update_or_create(
                name=data['name'],
                defaults={
                    'name_ru': data['name_ru'],
                    'dimension': dim,
                    'temperature': 0.5,
                },
            )
            stats.created += created
            stats.updated += not created
        return stats

    def import_effects(self) -> ImportStats:
        stats = ImportStats()
        html = self.client.fetch('id-effektov/')
        for data in parse_effects_page(html):
            if self.dry_run:
                stats.created += 1
                continue
            obj, created = Effect.objects.update_or_create(
                effect_id=data['effect_id'],
                defaults={
                    'name': data['name'],
                    'name_en': data['name_en'],
                    'numeric_id_je': data.get('numeric_id_je'),
                    'numeric_id_be': data.get('numeric_id_be'),
                },
            )
            if self.version:
                obj.versions.add(self.version)
            stats.created += created
            stats.updated += not created
        return stats

    def import_enchantments(self) -> ImportStats:
        stats = ImportStats()
        html = self.client.fetch('id-zacharovanij/')
        for data in parse_enchantments_page(html):
            if self.dry_run:
                stats.created += 1
                continue
            obj, created = Enchantment.objects.update_or_create(
                enchantment_id=data['enchantment_id'],
                defaults={
                    'name': data['name'],
                    'name_en': data['name_en'],
                    'numeric_id_je': data.get('numeric_id_je'),
                    'numeric_id_be': data.get('numeric_id_be'),
                    'max_level': data.get('max_level', 1),
                },
            )
            if self.version:
                obj.versions.add(self.version)
            stats.created += created
            stats.updated += not created
        return stats

    def import_structures(self) -> ImportStats:
        stats = ImportStats()
        html = self.client.fetch('komanda-locate/')
        for data in parse_structures_from_locate(html):
            if self.dry_run:
                stats.created += 1
                continue
            dim = self.dimensions.get(data['dimension'])
            obj, created = Structure.objects.update_or_create(
                structure_id=data['structure_id'],
                defaults={
                    'name': data['name'],
                    'name_en': data['name_en'],
                    'rarity': 'common',
                    'description': data.get('description', ''),
                    'images': [],
                },
            )
            if dim:
                obj.dimensions.add(dim)
            if self.version:
                obj.versions.add(self.version)
            stats.created += created
            stats.updated += not created
        return stats

    def import_items(self) -> ImportStats:
        stats = ImportStats()
        seen_ids: set[str] = set()

        for post in iter_posts(self.client, GROUP_CATEGORY):
            slug = post.get('slug', '')
            link = post.get('link', '')
            if not slug or not link:
                continue
            try:
                html = self.client.fetch(link)
                for data in parse_group_page(html, slug):
                    if data['item_id'] in seen_ids:
                        continue
                    seen_ids.add(data['item_id'])
                    s = self._upsert_item(data)
                    stats.merge(s)
            except Exception as exc:
                stats.errors.append(f"Group {slug}: {exc}")

        for post in iter_posts(self.client, PREDMET_CATEGORY):
            title = post.get('title', {}).get('rendered', '')
            link = post.get('link', '')
            slug = post.get('slug', '')
            if not link:
                continue
            item_id = None
            if self.deep:
                try:
                    html = self.client.fetch(link)
                    detail = parse_item_detail(html, title)
                    item_id = detail.get('item_id')
                    if item_id:
                        data = {
                            'item_id': item_id,
                            'name': detail.get('name') or title,
                            'name_en': detail.get('name_en', ''),
                            'category': category_from_group_slug(slug),
                            'description': detail.get('description', ''),
                        }
                        if item_id not in seen_ids:
                            seen_ids.add(item_id)
                            stats.merge(self._upsert_item(data))
                        else:
                            stats.merge(self._upsert_item(data, update_only=True))
                except Exception as exc:
                    stats.errors.append(f"Item {slug}: {exc}")
            else:
                bare_slug = slug.replace('-', '_')
                item_id = normalize_item_id(bare_slug)
                if item_id in seen_ids:
                    continue
                seen_ids.add(item_id)
                stats.merge(self._upsert_item({
                    'item_id': item_id,
                    'name': title,
                    'name_en': bare_slug.replace('_', ' ').title(),
                    'category': 'material',
                }))

        self._refresh_item_lookup()
        return stats

    def _upsert_item(self, data: dict, update_only: bool = False) -> ImportStats:
        stats = ImportStats()
        item_id = data.get('item_id')
        if not item_id:
            stats.skipped += 1
            return stats
        if self.dry_run:
            stats.created += 1
            return stats
        defaults = {
            'name': data.get('name', item_id),
            'name_en': data.get('name_en', ''),
            'category': data.get('category', 'material'),
            'description': data.get('description', ''),
            'stack_size': data.get('stack_size', 64),
            'rarity': data.get('rarity', 'common'),
        }
        if update_only:
            try:
                obj = Item.objects.get(item_id=item_id)
                for k, v in defaults.items():
                    if v:
                        setattr(obj, k, v)
                obj.save()
                stats.updated += 1
            except Item.DoesNotExist:
                stats.skipped += 1
            return stats
        obj, created = Item.objects.update_or_create(item_id=item_id, defaults=defaults)
        if self.version:
            obj.versions.add(self.version)
        stats.created += created
        stats.updated += not created
        return stats

    def _refresh_item_lookup(self):
        self.item_by_name = {}
        for item in Item.objects.all():
            self.item_by_name[item.name.lower()] = item
            bare = item.item_id.replace('minecraft:', '').replace('_', ' ')
            self.item_by_name[bare.lower()] = item

    def import_mobs(self) -> ImportStats:
        stats = ImportStats()
        html = self.client.fetch('id-mobov/')
        mob_list = parse_mobs_list_page(html)
        wp_slugs = {p['slug']: p['link'] for p in iter_posts(self.client, MOB_CATEGORY)}

        for base in mob_list:
            slug = base['mob_id'].replace('minecraft:', '').replace('_', '-')
            link = wp_slugs.get(slug)
            if not link:
                for s, url in wp_slugs.items():
                    if s.replace('-', '_') == base['mob_id'].replace('minecraft:', '').replace('_', '-'):
                        link = url
                        break
            data = dict(base)
            if self.deep and link:
                try:
                    detail_html = self.client.fetch(link)
                    data = parse_mob_detail(detail_html, base)
                except Exception as exc:
                    stats.errors.append(f"Mob {base['mob_id']}: {exc}")
            stats.merge(self._upsert_mob(data))
        return stats

    def _upsert_mob(self, data: dict) -> ImportStats:
        stats = ImportStats()
        mob_id = data.get('mob_id')
        if not mob_id:
            stats.skipped += 1
            return stats
        if self.dry_run:
            stats.created += 1
            return stats

        defaults = {
            'name': data.get('name', mob_id),
            'name_en': data.get('name_en', ''),
            'health': data.get('health', 10.0),
            'damage': data.get('damage', 0.0),
            'behavior': data.get('behavior', 'hostile'),
            'category': data.get('category', 'monster'),
            'experience': data.get('experience', 0),
            'description': data.get('description', ''),
        }
        mob, created = Mob.objects.update_or_create(mob_id=mob_id, defaults=defaults)
        if self.version:
            mob.versions.add(self.version)
        dim = self.dimensions.get('Overworld')
        if dim:
            mob.spawns_in.add(dim)
        stats.created += created
        stats.updated += not created

        if self.deep:
            stats.merge(self._import_mob_loot(mob, data.get('loot', [])))
            stats.merge(self._import_mob_spawn(mob, data.get('spawn')))
        return stats

    def _import_mob_loot(self, mob: Mob, loot_list: list) -> ImportStats:
        stats = ImportStats()
        if self.dry_run:
            return stats
        for drop in loot_list:
            item_name = drop.get('item_name', '').lower()
            item = self.item_by_name.get(item_name)
            if not item:
                for name, obj in self.item_by_name.items():
                    if item_name in name or name in item_name:
                        item = obj
                        break
            if not item:
                stats.skipped += 1
                continue
            _, created = LootDrop.objects.update_or_create(
                mob=mob,
                item=item,
                defaults={
                    'min_count': drop.get('min_count', 0),
                    'max_count': drop.get('max_count', 1),
                    'chance': drop.get('chance', 1.0),
                },
            )
            stats.created += created
            stats.updated += not created
        return stats

    def _import_mob_spawn(self, mob: Mob, spawn: dict | None) -> ImportStats:
        stats = ImportStats()
        if not spawn or self.dry_run:
            return stats
        dim = self.dimensions.get(spawn.get('dimension', 'Overworld'))
        if not dim:
            return stats
        MobSpawnCondition.objects.update_or_create(
            mob=mob,
            dimension=dim,
            defaults={
                'light_level_max': spawn.get('light_level_max', 7),
                'only_at_night': spawn.get('only_at_night', False),
            },
        )
        stats.created += 1
        return stats

    def import_recipes(self) -> ImportStats:
        stats = ImportStats()
        if not self.item_by_name:
            self._refresh_item_lookup()

        for post in iter_posts(self.client, PREDMET_CATEGORY):
            link = post.get('link', '')
            slug = post.get('slug', '')
            title = post.get('title', {}).get('rendered', '')
            if not link or not slug:
                continue
            bare = slug.replace('-', '_')
            item_id = normalize_item_id(bare)
            try:
                item = Item.objects.get(item_id=item_id)
            except Item.DoesNotExist:
                try:
                    item = Item.objects.filter(name=title).first()
                except Exception:
                    item = None
            if not item:
                stats.skipped += 1
                continue
            try:
                html = self.client.fetch(link)
            except Exception as exc:
                stats.errors.append(f"Recipe fetch {item.item_id}: {exc}")
                continue
            for recipe_data in parse_item_recipes(html, item.item_id, page_slug=slug):
                stats.merge(self._upsert_recipe(recipe_data))
        return stats

    def _upsert_recipe(self, data: dict) -> ImportStats:
        stats = ImportStats()
        if self.dry_run:
            stats.created += 1
            return stats
        try:
            result_item = Item.objects.get(item_id=data['result_item_id'])
        except Item.DoesNotExist:
            stats.skipped += 1
            return stats

        ing_key = '|'.join(sorted(i['item_id'] for i in data.get('ingredients', [])))
        recipe, created = Recipe.objects.update_or_create(
            result_item=result_item,
            recipe_type=data['recipe_type'],
            group=ing_key,
            defaults={
                'result_count': data.get('result_count', 1),
                'shape': data.get('shape'),
            },
        )
        if self.version:
            recipe.versions.add(self.version)

        for ing in data.get('ingredients', []):
            try:
                ing_item = Item.objects.get(item_id=ing['item_id'])
            except Item.DoesNotExist:
                stats.skipped += 1
                continue
            RecipeIngredient.objects.update_or_create(
                recipe=recipe,
                item=ing_item,
                position_row=ing.get('position_row'),
                position_col=ing.get('position_col'),
                defaults={'count': ing.get('count', 1)},
            )
        stats.created += created
        stats.updated += not created
        return stats
