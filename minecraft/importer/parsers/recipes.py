import re

from bs4 import BeautifulSoup, Tag

from importer.mappers import normalize_item_id
from importer.parsers.html import extract_give_id, make_soup


def parse_item_recipes(html: str, result_item_id: str, page_slug: str = '') -> list[dict]:
    soup = make_soup(html)
    if not page_slug:
        page_slug = result_item_id.replace('minecraft:', '').replace('_', '-')
    recipes = []
    in_section = False

    for heading in soup.find_all(['h2', 'h3', 'h4']):
        title = heading.get_text(' ', strip=True).lower()

        if heading.name == 'h2':
            if 'как создать' in title:
                in_section = True
                continue
            if in_section:
                break

        if not in_section or heading.name != 'h3':
            continue

        if 'печ' in title or 'плав' in title or 'копт' in title:
            for recipe in _parse_furnace_table(heading, result_item_id, page_slug):
                recipes.append(recipe)
        elif 'крафт' in title:
            for recipe in _parse_craft_table(heading, result_item_id, page_slug):
                recipes.append(recipe)

    return recipes


def _item_id_from_href(href: str) -> str | None:
    if not href or href.startswith('#') or 'category/' in href:
        return None
    slug = href.rstrip('/').split('/')[-1]
    if not slug:
        return None
    return normalize_item_id(slug.replace('-', '_'))


def _href_matches_page(href: str, page_slug: str) -> bool:
    slug = href.rstrip('/').split('/')[-1]
    return slug == page_slug


def _rows_for_heading(heading: Tag) -> list[Tag]:
    rows = []
    sibling = heading.find_next_sibling()
    while sibling and sibling.name not in ('h2', 'h3', 'h4'):
        if sibling.name == 'table':
            rows.extend(sibling.find_all('tr'))
        elif sibling.name == 'tr':
            rows.append(sibling)
        sibling = sibling.find_next_sibling()
    return rows


def _parse_craft_table(heading: Tag, result_item_id: str, page_slug: str) -> list[dict]:
    recipes = []
    for tr in _rows_for_heading(heading):
        links = tr.find_all('a', href=True)
        if not links:
            continue
        ids = []
        seen_ing = set()
        is_result_row = False
        for link in links:
            href = link['href']
            if _href_matches_page(href, page_slug):
                is_result_row = True
            item_id = extract_give_id(tr.get_text(' ')) or _item_id_from_href(href)
            if item_id and not _href_matches_page(href, page_slug) and item_id not in seen_ing:
                seen_ing.add(item_id)
                ids.append({'item_id': item_id, 'count': 1})
        if is_result_row and ids:
            recipes.append({
                'result_item_id': result_item_id,
                'result_count': 1,
                'recipe_type': 'crafting_3x3',
                'shape': None,
                'ingredients': ids,
            })
    return recipes


def _parse_furnace_table(heading: Tag, result_item_id: str, page_slug: str) -> list[dict]:
    title = heading.get_text(' ').lower()
    recipe_type = 'smelting'
    if 'плавильн' in title:
        recipe_type = 'blasting'
    elif 'копт' in title:
        recipe_type = 'smoking'

    recipes = []
    for tr in _rows_for_heading(heading):
        links = tr.find_all('a', href=True)
        if not links:
            continue
        ingredients = []
        is_result = False
        for link in links:
            href = link['href']
            if _href_matches_page(href, page_slug):
                is_result = True
            else:
                item_id = _item_id_from_href(href)
                if item_id:
                    ingredients.append({'item_id': item_id, 'count': 1})
        if is_result and ingredients:
            recipes.append({
                'result_item_id': result_item_id,
                'result_count': 1,
                'recipe_type': recipe_type,
                'shape': None,
                'ingredients': ingredients[:1],
            })
    return recipes
