import re
from typing import Optional

from bs4 import BeautifulSoup, Tag

from importer.mappers import map_recipe_type, minecraft_item_id


def parse_item_recipe_sections(soup: BeautifulSoup, result_item_id: str) -> list[dict]:
    recipes = []
    for heading in soup.find_all(['h3', 'h4']):
        title = heading.get_text(strip=True)
        lower = title.lower()
        if not any(k in lower for k in ('крафт', 'печ', 'плав', 'копт', 'кост', 'кузн', 'камнерез', 'вароч')):
            continue
        table = heading.find_next('table')
        if not table:
            continue
        recipe_type = map_recipe_type(title)
        ingredients = _parse_recipe_table(table)
        if ingredients:
            recipes.append({
                'result_item_id': result_item_id,
                'recipe_type': recipe_type,
                'result_count': 1,
                'ingredients': ingredients,
                'shape': None,
            })
    return recipes


def _parse_recipe_table(table: Tag) -> list[dict]:
    ingredients = []
    for row in table.find_all('tr'):
        cells = row.find_all('td')
        for cell in cells:
            link = cell.find('a', href=True)
            if not link:
                text = cell.get_text(strip=True)
                if text.isdigit():
                    continue
            if link:
                slug = link['href'].rstrip('/').split('/')[-1]
                name = link.get_text(strip=True)
                count_match = re.search(r'(\d+)', cell.get_text())
                count = int(count_match.group(1)) if count_match else 1
                ingredients.append({
                    'item_id': minecraft_item_id(slug.replace('-', '_')),
                    'item_slug': slug,
                    'name': name,
                    'count': count,
                })
    return ingredients


def scrape_recipes_page(html: str) -> list[dict]:
    """Parse recipes from Playwright-rendered /recepty/ HTML."""
    soup = BeautifulSoup(html, 'lxml')
    recipes = []
    for row in soup.select('table tr'):
        cells = row.find_all('td')
        if len(cells) < 2:
            continue
        result_link = cells[0].find('a', href=True)
        if not result_link:
            continue
        result_slug = result_link['href'].rstrip('/').split('/')[-1]
        result_id = minecraft_item_id(result_slug.replace('-', '_'))
        ingredients = []
        for link in cells[1].find_all('a', href=True):
            slug = link['href'].rstrip('/').split('/')[-1]
            ingredients.append({
                'item_id': minecraft_item_id(slug.replace('-', '_')),
                'item_slug': slug,
                'name': link.get_text(strip=True),
                'count': 1,
            })
        if ingredients:
            recipes.append({
                'result_item_id': result_id,
                'recipe_type': 'crafting_3x3',
                'result_count': 1,
                'ingredients': ingredients,
                'shape': None,
            })
    return recipes


def fetch_recipes_with_playwright(url: str, timeout_ms: int = 60000) -> str:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise ImportError(
            'playwright не установлен. Выполните: pip install playwright && '
            'playwright install chromium'
        ) from exc

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until='networkidle', timeout=timeout_ms)
        page.wait_for_selector('table tr td a', timeout=timeout_ms)
        html = page.content()
        browser.close()
    return html
