from pathlib import Path

import pytest

from importer.parsers.biomes import parse_biomes_page
from importer.parsers.items import parse_group_page
from importer.parsers.mobs import parse_mob_detail, parse_mobs_list_page
from importer.parsers.recipes import parse_item_recipes

FIXTURES = Path(__file__).parent / 'fixtures'


def _read(name: str) -> str:
    return (FIXTURES / name).read_text(encoding='utf-8')


def test_parse_biomes():
    biomes = parse_biomes_page(_read('biomy_snippet.html'))
    assert len(biomes) == 3
    assert biomes[0]['name_ru'] == 'Равнины'
    assert biomes[0]['dimension'] == 'Overworld'
    assert biomes[1]['dimension'] == 'Nether'


def test_parse_mobs_list():
    mobs = parse_mobs_list_page(_read('id_mobov_snippet.html'))
    assert len(mobs) == 2
    assert mobs[0]['mob_id'] == 'minecraft:zombie'
    assert mobs[0]['behavior'] == 'hostile'


def test_parse_group_items():
    items = parse_group_page(_read('ingredienty_snippet.html'), 'ingredienty')
    assert len(items) == 2
    assert items[0]['item_id'] == 'minecraft:iron_ingot'
    assert items[0]['category'] == 'material'


def test_parse_mob_detail():
    mob = parse_mob_detail(_read('zombi_snippet.html'), {'mob_id': 'minecraft:zombie', 'behavior': 'hostile'})
    assert mob['health'] == 20.0
    assert mob['experience'] == 5
    assert len(mob['loot']) >= 1


def test_parse_recipes():
    recipes = parse_item_recipes(
        _read('iron_ingot_recipes.html'),
        'minecraft:iron_ingot',
        'zheleznyj-slitok',
    )
    assert len(recipes) >= 2
    types = {r['recipe_type'] for r in recipes}
    assert 'crafting_3x3' in types
    assert 'smelting' in types
