import re
from datetime import date
from typing import Optional

from bs4 import BeautifulSoup, Tag

from importer.mappers import normalize_version_number

MONTHS_RU = {
    'января': 1, 'февраля': 2, 'марта': 3, 'апреля': 4,
    'мая': 5, 'июня': 6, 'июля': 7, 'августа': 8,
    'сентября': 9, 'октября': 10, 'ноября': 11, 'декабря': 12,
}


def _parse_ru_date(text: str) -> Optional[date]:
    text = text.strip().lower()
    match = re.search(r'(\d{1,2})\s+(\w+)\s+(\d{4})', text)
    if not match:
        return None
    day, month_name, year = match.groups()
    month = MONTHS_RU.get(month_name)
    if not month:
        return None
    return date(int(year), month, int(day))


def parse_home_versions(soup: BeautifulSoup) -> list[dict]:
    versions = []
    for table in soup.find_all('table'):
        headers = [th.get_text(strip=True).lower() for th in table.find_all('th')]
        if not headers or 'версия' not in ' '.join(headers):
            continue
        for row in table.find_all('tr'):
            cells = row.find_all(['td', 'th'])
            if len(cells) < 2:
                continue
            date_text = cells[0].get_text(' ', strip=True)
            version_cell = cells[1]
            link = version_cell.find('a', href=True)
            version_text = (
                link.get_text(strip=True) if link else version_cell.get_text(strip=True)
            )
            version_number = normalize_version_number(version_text)
            if not re.match(r'\d', version_number):
                continue
            release = _parse_ru_date(date_text) or date(2011, 11, 18)
            slug = ''
            if link and link.get('href'):
                slug = link['href'].rstrip('/').split('/')[-1]
            versions.append({
                'version_number': version_number,
                'release_date': release,
                'slug': slug,
                'english_name': cells[2].get_text(strip=True) if len(cells) > 2 else '',
            })
        if versions:
            break
    return versions


def parse_version_article_meta(soup: BeautifulSoup) -> Optional[date]:
    text = soup.get_text(' ', strip=True)[:2000]
    patterns = [
        r'вышел[а]?\s+(\d{1,2}\s+\w+\s+\d{4})',
        r'вышла\s+(\d{1,2}\s+\w+\s+\d{4})',
        r'(\d{1,2}\s+\w+\s+\d{4})\s+года',
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            parsed = _parse_ru_date(match.group(1))
            if parsed:
                return parsed
    return None


def version_slug_for_number(version_number: str) -> str:
    major = version_number.split('.')
    if len(major) >= 2:
        return f'minecraft-{major[0]}-{major[1]}'
    return f'minecraft-{version_number.replace(".", "-")}'
