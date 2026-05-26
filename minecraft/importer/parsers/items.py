import re
<<<<<<< HEAD

from importer.client import GIVE_RE
from importer.mappers import category_from_group_slug, normalize_item_id
from importer.parsers.html import (
    extract_give_id,
    first_paragraph,
    id_to_title,
    make_soup,
    parse_key_value_table,
    parse_tables,
    parse_version_added,
    slug_from_url,
)


def parse_group_page(html: str, group_slug: str) -> list[dict]:
    soup = make_soup(html)
    category = category_from_group_slug(group_slug)
    items = []
    for table in parse_tables(soup):
        for row in table:
            row_text = ' '.join(row)
            item_id = extract_give_id(row_text)
            if not item_id:
                continue
            name = row[0].strip() if row else id_to_title(item_id)
            if name.startswith('/give'):
                continue
            items.append({
                'item_id': normalize_item_id(item_id),
                'name': name,
                'name_en': id_to_title(item_id.replace('minecraft:', '')),
                'category': category,
            })
    return items


def parse_item_detail(html: str, fallback_name: str = '') -> dict:
    soup = make_soup(html)
    text = soup.get_text(' ', strip=True)
    item_id = None
    match = re.search(r'текстовым ID\s+([\w]+)', text, re.I)
    if match:
        item_id = normalize_item_id(match.group(1))
    if not item_id:
        for code in soup.find_all(string=GIVE_RE):
            m = GIVE_RE.search(str(code))
            if m:
                item_id = normalize_item_id(m.group(1))
                break
    h1 = soup.find('h1')
    name = h1.get_text(strip=True) if h1 else fallback_name
    info = {}
    for table in parse_tables(soup):
        if len(table) == 2 and len(table[0]) == 2 and len(table[1]) == 2:
            kv = parse_key_value_table(table)
            if 'id' in str(kv).lower() or 'добавлен' in str(kv).lower():
                info.update(kv)
    version = None
    for key, val in info.items():
        if 'добавлен' in key.lower():
            version = parse_version_added(val)
    return {
        'item_id': item_id,
        'name': name,
        'name_en': id_to_title((item_id or '').replace('minecraft:', '')),
        'description': first_paragraph(soup),
        'version': version,
    }
=======
from typing import Optional

from bs4 import BeautifulSoup, Tag

from importer.client import HttpClient
from importer.mappers import map_item_category, minecraft_item_id, normalize_version_number

ITEM_ID_PATTERNS = [
    re.compile(r'ID\s*["\']([^"\']+)["\']', re.I),
    re.compile(r'текстовым ID\s+([\w:]+)', re.I),
    re.compile(r'предмет с ID\s+["\']?([\w:{}"]+)', re.I),
]
ADDED_VERSION_PATTERN = re.compile(
    r'добавлен[а]?\s+в\s+(.+?)\s+верси',
    re.I,
)


def collect_item_slugs_from_wp(client: HttpClient, category_id: int = 3) -> list[dict]:
    slugs = []
    page = 1
    while True:
        posts = client.fetch_wp_posts(category_id, page=page, per_page=100)
        if not posts:
            break
        for post in posts:
            slugs.append({
                'slug': post.get('slug', ''),
                'title': post.get('title', {}).get('rendered', ''),
                'link': post.get('link', ''),
            })
        if len(posts) < 100:
            break
        page += 1
    return slugs


def _first_paragraph(soup: BeautifulSoup) -> str:
    article = soup.find('article') or soup.find(class_=re.compile(r'entry|content|post'))
    if not article:
        article = soup
    for p in article.find_all('p'):
        text = p.get_text(' ', strip=True)
        if len(text) > 30:
            return text
    return ''


def _extract_item_id(text: str) -> Optional[str]:
    for pattern in ITEM_ID_PATTERNS:
        match = pattern.search(text)
        if match:
            raw = match.group(1).strip().strip('"')
            if raw and len(raw) < 120:
                return minecraft_item_id(raw.split()[0])
    return None


def _extract_added_version(text: str) -> Optional[str]:
    match = ADDED_VERSION_PATTERN.search(text)
    if match:
        return normalize_version_number(match.group(1))
    return None


def _guess_category(soup: BeautifulSoup, text: str) -> str:
    for link in soup.find_all('a', href=True):
        href = link['href'].lower()
        label = link.get_text(strip=True).lower()
        if '/category/' in href or '/ingredient' in href:
            return map_item_category(label)
    lower = text.lower()
    if 'блок' in lower[:200]:
        return 'block'
    if 'оружие' in lower or 'меч' in lower:
        return 'weapon'
    if 'броня' in lower or 'шлем' in lower:
        return 'armor'
    if 'инструмент' in lower:
        return 'tool'
    return 'material'


def parse_item_page(soup: BeautifulSoup, slug: str, fallback_title: str = '') -> dict:
    title_el = soup.find('h1')
    name = title_el.get_text(strip=True) if title_el else fallback_title
    name = re.sub(r'\s*-\s*Minecraft.*$', '', name, flags=re.I).strip()
    body_text = soup.get_text(' ', strip=True)
    item_id = _extract_item_id(body_text)
    if not item_id:
        item_id = minecraft_item_id(slug.replace('-', '_')[:50])
    added_version = _extract_added_version(body_text)
    description = _first_paragraph(soup)
    icon = ''
    img = soup.find('img', src=re.compile(r'\.(png|webp|gif)', re.I))
    if img and img.get('src'):
        icon = img['src']
        if icon.startswith('/'):
            icon = f'https://idpredmetov.ru{icon}'
    return {
        'slug': slug,
        'item_id': item_id,
        'name': name or fallback_title,
        'name_en': slug.replace('-', ' ').title(),
        'description': description,
        'icon_path': icon,
        'category': _guess_category(soup, body_text),
        'added_in_version': added_version,
        'stack_size': 64,
        'rarity': 'common',
    }


def parse_version_new_items(soup: BeautifulSoup, version_number: str) -> list[dict]:
    items = []
    in_items_section = False
    for el in soup.find_all(['h2', 'h3', 'table', 'p']):
        if el.name in ('h2', 'h3'):
            title = el.get_text(strip=True).lower()
            in_items_section = 'предмет' in title or 'блок' in title
            continue
        if not in_items_section or el.name != 'table':
            continue
        for row in el.find_all('tr'):
            cells = row.find_all('td')
            if len(cells) < 2:
                continue
            link = cells[0].find('a', href=True)
            name = link.get_text(strip=True) if link else cells[0].get_text(strip=True)
            raw_id = cells[1].get_text(strip=True)
            if not name or not raw_id or raw_id.lower() == 'id':
                continue
            if len(raw_id) > 100:
                continue
            items.append({
                'name': name,
                'item_id': minecraft_item_id(raw_id),
                'added_in_version': version_number,
                'slug': link['href'].rstrip('/').split('/')[-1] if link else '',
            })
    return items
>>>>>>> 846cf762af40ade9e079b9d382b3e18f8ab82502
