<<<<<<< HEAD
from pathlib import Path

import pytest

from importer.parsers.biomes import parse_biomes_page
from importer.parsers.items import parse_group_page
from importer.parsers.mobs import parse_mob_detail, parse_mobs_list_page
from importer.parsers.recipes import parse_item_recipes
=======
from datetime import date
from pathlib import Path

import pytest
from bs4 import BeautifulSoup

from importer.mappers import biome_dimension_key, map_behavior, normalize_version_number
from importer.parsers.biomes import parse_biomes_page
from importer.parsers.items import parse_item_page
from importer.parsers.mobs import parse_mob_detail_page, parse_mobs_index_page
from importer.parsers.versions import parse_home_versions
>>>>>>> 846cf762af40ade9e079b9d382b3e18f8ab82502

FIXTURES = Path(__file__).parent / 'fixtures'


<<<<<<< HEAD
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
=======
def _load(name: str) -> BeautifulSoup:
    html = (FIXTURES / name).read_text(encoding='utf-8')
    return BeautifulSoup(html, 'lxml')


def test_parse_item_page_diamond():
    data = parse_item_page(_load('almaz.html'), 'almaz', 'Алмаз')
    assert data['item_id'] == 'minecraft:diamond'
    assert data['added_in_version'] in ('1', '1.0.0')
    assert data['name'].startswith('Алмаз')


def test_parse_mob_detail_zombie():
    index = {'slug': 'zombi', 'mob_id': 'minecraft:zombie', 'behavior': 'hostile', 'name': 'Зомби'}
    data = parse_mob_detail_page(_load('zombi.html'), index)
    assert data['mob_id'] == 'minecraft:zombie'
    assert data['health'] == 20.0
    assert data['intro_version'] == '1.0.0'
    assert map_behavior('Враждебный') == 'hostile'


def test_parse_biomes():
    biomes = parse_biomes_page(_load('biomy.html'))
    assert len(biomes) == 2
    assert biomes[0]['name'] == 'plains'
    assert biomes[1]['dimension_key'] == 'Nether'
    assert biome_dimension_key('nether_wastes') == 'Nether'


def test_normalize_version():
    assert normalize_version_number('1-й') == '1.0.0'
    assert normalize_version_number('1.21.2') == '1.21.2'


def test_parse_home_versions_table():
    html = """
    <table>
    <tr><th>Дата</th><th>Версия</th><th>Название</th></tr>
    <tr><td>13 июня 2024</td><td><a href="/minecraft-1-21/">1.21</a></td><td>Tricky Trials</td></tr>
    </table>
    """
    versions = parse_home_versions(BeautifulSoup(html, 'lxml'))
    assert len(versions) == 1
    assert versions[0]['version_number'] == '1.21'
    assert versions[0]['release_date'] == date(2024, 6, 13)


def test_parse_mobs_index_minimal():
    html = """
    <table>
    <tr><td><a href="/zombi/">Зомби</a></td><td>Враждебный</td><td>Нет</td><td>zombie</td></tr>
    </table>
    """
    mobs = parse_mobs_index_page(BeautifulSoup(html, 'lxml'))
    assert len(mobs) == 1
    assert mobs[0]['mob_id'] == 'minecraft:zombie'
>>>>>>> 846cf762af40ade9e079b9d382b3e18f8ab82502
