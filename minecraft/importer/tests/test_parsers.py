from datetime import date
from pathlib import Path

import pytest
from bs4 import BeautifulSoup

from importer.mappers import biome_dimension_key, map_behavior, normalize_version_number
from importer.parsers.biomes import parse_biomes_page
from importer.parsers.items import parse_item_page
from importer.parsers.mobs import parse_mob_detail_page, parse_mobs_index_page
from importer.parsers.versions import parse_home_versions

FIXTURES = Path(__file__).parent / 'fixtures'


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
