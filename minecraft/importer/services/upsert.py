from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Optional

from django.conf import settings
from django.db import transaction

from biomes.models import Biome
from dimensions.models import Dimension
from items.models import Item
from loot_drops.models import LootDrop
from mobs.models import Mob
from recipe_ingredients.models import RecipeIngredient
from recipes.models import Recipe
from structures.models import Structure
from versions.models import MinecraftVersion

from importer.client import HttpClient
from importer.parsers import (
    collect_item_slugs_from_wp,
    parse_biomes_page,
    parse_home_versions,
    parse_item_page,
    parse_item_recipe_sections,
    parse_mob_detail_page,
    parse_mobs_index_page,
    parse_version_article_meta,
    parse_version_new_items,
    parse_version_structures,
    scrape_recipes_page,
)
from importer.parsers.loot import parse_mob_drops
from importer.parsers.recipes import fetch_recipes_with_playwright
from importer.parsers.versions import version_slug_for_number
from importer.services.version_propagate import propagate_versions
from importer.stats import ScrapeStats, StatsDisplay


@dataclass
class ImportContext:
    client: HttpClient
    stats: ScrapeStats
    display: StatsDisplay
    dry_run: bool = False
    skip_existing: bool = False
    limit_items: Optional[int] = None
    mob_intro: dict[str, str] = field(default_factory=dict)
    structure_intro: dict[str, str] = field(default_factory=dict)
    cache_dir: Path = field(default_factory=lambda: Path(settings.BASE_DIR) / 'importer' / 'cache')

    def version_by_number(self) -> dict[str, MinecraftVersion]:
        return {v.version_number: v for v in MinecraftVersion.objects.all()}

    def resolve_version(self, number: str | None) -> MinecraftVersion | None:
        if not number:
            return None
        versions = self.version_by_number()
        if number in versions:
            return versions[number]
        parts = number.split('.')
        while len(parts) > 1:
            parts.pop()
            candidate = '.'.join(parts)
            if candidate in versions:
                return versions[candidate]
        return versions.get('1.0.0')


def _ensure_cache_dir(ctx: ImportContext):
    ctx.cache_dir.mkdir(parents=True, exist_ok=True)


def seed_dimensions(ctx: ImportContext) -> dict[str, Dimension]:
    ctx.stats.set_stage('dimensions')
    ctx.display.refresh()
    defaults = [
        ('Overworld', 'Верхний мир'),
        ('Nether', 'Нижний мир'),
        ('End', 'Край'),
    ]
    result = {}
    for name, name_ru in defaults:
        if ctx.dry_run:
            continue
        dim, _ = Dimension.objects.get_or_create(
            name=name,
            defaults={'name_ru': name_ru, 'description': ''},
        )
        result[name] = dim
        ctx.stats.dimensions += 1
    ctx.display.refresh()
    return result


def import_versions(ctx: ImportContext):
    ctx.stats.set_stage('versions')
    ctx.display.refresh()
    soup = ctx.client.get_soup('/')
    parsed = parse_home_versions(soup)
    if not parsed:
        parsed = [
            {'version_number': '1.21', 'release_date': date(2024, 6, 13), 'slug': 'minecraft-1-21'},
            {'version_number': '1.0.0', 'release_date': date(2011, 11, 18), 'slug': 'minecraft-1-0'},
        ]
    if ctx.dry_run:
        ctx.stats.versions = len(parsed)
        return
    MinecraftVersion.objects.update(is_latest=False)
    latest_date = max(v['release_date'] for v in parsed)
    for entry in parsed:
        slug = entry.get('slug') or version_slug_for_number(entry['version_number'])
        try:
            article_soup = ctx.client.get_soup(f'/{slug}/')
            article_date = parse_version_article_meta(article_soup)
            if article_date:
                entry['release_date'] = article_date
        except Exception:
            ctx.stats.errors += 1
        is_latest = entry['release_date'] == latest_date
        MinecraftVersion.objects.update_or_create(
            version_number=entry['version_number'],
            defaults={
                'release_date': entry['release_date'],
                'is_latest': is_latest,
            },
        )
        ctx.stats.versions += 1
        ctx.display.refresh()


def import_biomes(ctx: ImportContext, dimensions: dict[str, Dimension]):
    ctx.stats.set_stage('biomes')
    ctx.display.refresh()
    soup = ctx.client.get_soup('/biomy/')
    parsed = parse_biomes_page(soup)
    for entry in parsed:
        if ctx.dry_run:
            ctx.stats.biomes += 1
            continue
        dim = dimensions.get(entry['dimension_key'])
        if not dim:
            continue
        Biome.objects.update_or_create(
            name=entry['name'],
            defaults={
                'name_ru': entry['name_ru'],
                'dimension': dim,
                'temperature': entry['temperature'],
                'description': entry['description'],
            },
        )
        ctx.stats.biomes += 1
    ctx.display.refresh()


def import_items(ctx: ImportContext):
    _ensure_cache_dir(ctx)
    slug_cache = ctx.cache_dir / 'item_slugs.json'
    ctx.stats.set_stage('items: slugs')
    if slug_cache.exists() and ctx.skip_existing:
        slugs = json.loads(slug_cache.read_text(encoding='utf-8'))
    else:
        slugs = collect_item_slugs_from_wp(ctx.client)
        if not ctx.dry_run:
            slug_cache.write_text(json.dumps(slugs, ensure_ascii=False), encoding='utf-8')

    if ctx.limit_items:
        slugs = slugs[: ctx.limit_items]

    total = len(slugs)
    ctx.stats.set_stage('items', 0, total)
    version_overrides: dict[str, str] = {}

    for idx, entry in enumerate(slugs, start=1):
        slug = entry['slug']
        ctx.display.tick(url=f'/{slug}/', current=idx)
        if not slug:
            ctx.stats.skipped += 1
            continue
        try:
            if ctx.skip_existing and not ctx.dry_run:
                exists = Item.objects.filter(item_id__icontains=slug.replace('-', '_')).exists()
                if exists:
                    ctx.stats.skipped += 1
                    continue
            soup = ctx.client.get_soup(f'/{slug}/')
            data = parse_item_page(soup, slug, entry.get('title', ''))
            if ctx.dry_run:
                ctx.stats.items += 1
                continue
            intro = ctx.resolve_version(data.get('added_in_version'))
            item, created = Item.objects.update_or_create(
                item_id=data['item_id'],
                defaults={
                    'name': data['name'][:100],
                    'name_en': data['name_en'][:100],
                    'description': data['description'],
                    'icon_path': data['icon_path'][:200],
                    'category': data['category'],
                    'stack_size': data['stack_size'],
                    'rarity': data['rarity'],
                    'added_in_version': intro,
                    'is_removed': False,
                },
            )
            if data.get('added_in_version'):
                version_overrides[data['item_id']] = data['added_in_version']
            ctx.stats.items += 1 if created else 0
            ctx.stats.items = Item.objects.count()
        except Exception:
            ctx.stats.errors += 1

    ctx.stats.set_stage('items: version tables')
    versions = list(MinecraftVersion.objects.order_by('-release_date')[:15])
    for ver in versions:
        slug = version_slug_for_number(ver.version_number)
        try:
            soup = ctx.client.get_soup(f'/{slug}/')
            for row in parse_version_new_items(soup, ver.version_number):
                version_overrides[row['item_id']] = ver.version_number
                if ctx.dry_run:
                    continue
                intro = ctx.resolve_version(ver.version_number)
                Item.objects.update_or_create(
                    item_id=row['item_id'],
                    defaults={
                        'name': row['name'][:100],
                        'name_en': row['item_id'].replace('minecraft:', '').replace('_', ' ').title()[:100],
                        'description': '',
                        'category': 'block',
                        'added_in_version': intro,
                    },
                )
        except Exception:
            ctx.stats.errors += 1

    if not ctx.dry_run:
        for item_id, ver_num in version_overrides.items():
            item = Item.objects.filter(item_id=item_id).first()
            intro = ctx.resolve_version(ver_num)
            if item and intro and (
                not item.added_in_version
                or item.added_in_version.release_date > intro.release_date
            ):
                item.added_in_version = intro
                item.save(update_fields=['added_in_version'])

    ctx.display.refresh()


def import_mobs(ctx: ImportContext):
    ctx.stats.set_stage('mobs')
    soup = ctx.client.get_soup('/id-mobov/')
    index = parse_mobs_index_page(soup)
    total = len(index)
    ctx.stats.set_stage('mobs', 0, total)

    for idx, entry in enumerate(index, start=1):
        slug = entry['slug']
        ctx.display.tick(url=f'/{slug}/', current=idx)
        try:
            if ctx.skip_existing and not ctx.dry_run:
                if Mob.objects.filter(mob_id=entry['mob_id']).exists():
                    ctx.stats.skipped += 1
                    continue
            detail_soup = ctx.client.get_soup(f'/{slug}/')
            data = parse_mob_detail_page(detail_soup, entry)
            if ctx.dry_run:
                ctx.stats.mobs += 1
                continue
            mob, _ = Mob.objects.update_or_create(
                mob_id=data['mob_id'],
                defaults={
                    'name': data['name'][:100],
                    'name_en': data['name_en'][:100],
                    'health': data['health'],
                    'damage': data['damage'],
                    'behavior': data['behavior'],
                    'category': data['category'],
                    'experience': data['experience'],
                    'description': data['description'] or '—',
                    'icon_path': data['icon_path'][:200],
                    'image_path': data['image_path'][:200],
                },
            )
            if data.get('intro_version'):
                ctx.mob_intro[data['mob_id']] = data['intro_version']
            ctx.stats.mobs = Mob.objects.count()

            drops = parse_mob_drops(detail_soup)
            for drop in drops:
                item = None
                if drop.get('item_id'):
                    item = Item.objects.filter(item_id=drop['item_id']).first()
                if not item and drop.get('item_slug'):
                    item = Item.objects.filter(
                        item_id__icontains=drop['item_slug'].replace('-', '_')
                    ).first()
                if not item:
                    continue
                if ctx.dry_run:
                    continue
                LootDrop.objects.update_or_create(
                    mob=mob,
                    item=item,
                    defaults={
                        'min_count': drop['min_count'],
                        'max_count': drop['max_count'],
                        'chance': drop['chance'],
                    },
                )
                ctx.stats.loot_drops = LootDrop.objects.count()
        except Exception:
            ctx.stats.errors += 1
    ctx.display.refresh()


def import_structures(ctx: ImportContext):
    ctx.stats.set_stage('structures')
    for ver in MinecraftVersion.objects.order_by('-release_date')[:12]:
        slug = version_slug_for_number(ver.version_number)
        try:
            soup = ctx.client.get_soup(f'/{slug}/')
            for data in parse_version_structures(soup, ver.version_number):
                if ctx.dry_run:
                    ctx.stats.structures += 1
                    continue
                structure, _ = Structure.objects.update_or_create(
                    structure_id=data['structure_id'],
                    defaults={
                        'name': data['name'][:100],
                        'name_en': data['name_en'][:100],
                        'description': data.get('description', data['name'])[:5000],
                        'rarity': data.get('rarity', 'uncommon'),
                        'images': [],
                    },
                )
                ctx.structure_intro[data['structure_id']] = data['intro_version']
                ctx.stats.structures = Structure.objects.count()
        except Exception:
            ctx.stats.errors += 1
    ctx.display.refresh()


def _save_recipe(ctx: ImportContext, recipe_data: dict):
    result = Item.objects.filter(item_id=recipe_data['result_item_id']).first()
    if not result:
        return
    recipe, _ = Recipe.objects.get_or_create(
        result_item=result,
        recipe_type=recipe_data['recipe_type'],
        defaults={
            'result_count': recipe_data.get('result_count', 1),
            'shape': recipe_data.get('shape'),
        },
    )
    intro = result.added_in_version
    if intro:
        recipe.versions.add(intro)
    for idx, ing in enumerate(recipe_data.get('ingredients', [])):
        ing_item = Item.objects.filter(item_id=ing['item_id']).first()
        if not ing_item:
            continue
        RecipeIngredient.objects.update_or_create(
            recipe=recipe,
            position_row=idx // 3,
            position_col=idx % 3,
            defaults={
                'item': ing_item,
                'count': ing.get('count', 1),
            },
        )
    ctx.stats.recipes = Recipe.objects.count()


def import_recipes(ctx: ImportContext):
    ctx.stats.set_stage('recipes: item pages')
    slug_cache = ctx.cache_dir / 'item_slugs.json'
    slug_entries = []
    if slug_cache.exists():
        slug_entries = json.loads(slug_cache.read_text(encoding='utf-8'))
    if ctx.limit_items:
        slug_entries = slug_entries[: ctx.limit_items]

    for entry in slug_entries:
        slug = entry.get('slug', '')
        if not slug:
            continue
        try:
            soup = ctx.client.get_soup(f'/{slug}/')
            data = parse_item_page(soup, slug, entry.get('title', ''))
            if not Item.objects.filter(item_id=data['item_id']).exists():
                continue
            for recipe_data in parse_item_recipe_sections(soup, data['item_id']):
                if not ctx.dry_run:
                    _save_recipe(ctx, recipe_data)
        except Exception:
            ctx.stats.errors += 1

    ctx.stats.set_stage('recipes: recepty (playwright)')
    ctx.display.refresh()
    try:
        html = fetch_recipes_with_playwright('https://idpredmetov.ru/recepty/')
        for recipe_data in scrape_recipes_page(html):
            if not ctx.dry_run:
                _save_recipe(ctx, recipe_data)
            else:
                ctx.stats.recipes += 1
    except Exception:
        ctx.stats.errors += 1
    ctx.display.refresh()


def run_import(
    dry_run: bool = False,
    skip_existing: bool = False,
    delay: float = 0.5,
    no_ui: bool = False,
    limit_items: Optional[int] = None,
):
    stats = ScrapeStats()
    client = HttpClient(delay=delay)
    display = StatsDisplay(stats, enabled=not no_ui)

    ctx = ImportContext(
        client=client,
        stats=stats,
        display=display,
        dry_run=dry_run,
        skip_existing=skip_existing,
        limit_items=limit_items,
    )

    with display:
        dimensions = seed_dimensions(ctx)
        import_versions(ctx)
        if not ctx.dry_run:
            dimensions = {
                d.name: d for d in Dimension.objects.all()
            }
        import_biomes(ctx, dimensions)
        import_items(ctx)
        import_mobs(ctx)
        import_structures(ctx)
        if not dry_run:
            import_recipes(ctx)
        if not dry_run:
            stats.set_stage('version propagate')
            display.refresh()
            propagate_versions(ctx.mob_intro, ctx.structure_intro)

    return stats
