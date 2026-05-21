import re
from typing import Any

from bs4 import BeautifulSoup

from importer.client import GIVE_RE, TEXT_ID_RE


def make_soup(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, 'lxml')


def slug_from_url(url: str) -> str:
    return url.rstrip('/').split('/')[-1]


def id_to_title(name: str) -> str:
    return name.replace('_', ' ').title()


def extract_give_id(text: str) -> str | None:
    match = GIVE_RE.search(text)
    if match:
        return match.group(1)
    match = TEXT_ID_RE.search(text)
    if match:
        return match.group(1)
    return None


def parse_tables(soup: BeautifulSoup) -> list[list[list[str]]]:
    tables = []
    for table in soup.find_all('table'):
        rows = []
        for tr in table.find_all('tr'):
            cells = [cell.get_text(' ', strip=True) for cell in tr.find_all(['th', 'td'])]
            if cells:
                rows.append(cells)
        if rows:
            tables.append(rows)
    return tables


def find_section_tables(soup: BeautifulSoup, heading_keywords: tuple[str, ...]) -> list[list[list[str]]]:
    for tag in soup.find_all(['h2', 'h3', 'h4']):
        title = tag.get_text(' ', strip=True).lower()
        if not any(kw in title for kw in heading_keywords):
            continue
        sibling = tag.find_next_sibling()
        while sibling:
            if sibling.name in ('h2', 'h3', 'h4'):
                break
            if sibling.name == 'table':
                rows = []
                for tr in sibling.find_all('tr'):
                    cells = [c.get_text(' ', strip=True) for c in tr.find_all(['th', 'td'])]
                    if cells:
                        rows.append(cells)
                if rows:
                    return [rows]
            sibling = sibling.find_next_sibling()
    return []


def parse_key_value_table(rows: list[list[str]]) -> dict[str, str]:
    result = {}
    for row in rows:
        if len(row) >= 2 and row[0] and row[1]:
            result[row[0].strip()] = row[1].strip()
    return result


def first_paragraph(soup: BeautifulSoup) -> str:
    for p in soup.find_all('p'):
        text = p.get_text(' ', strip=True)
        if len(text) > 40:
            return text
    return ''


def parse_version_added(text: str) -> str | None:
    match = re.search(r'(\d+\.\d+(?:\.\d+)?)', text)
    return match.group(1) if match else None


def parse_health_damage(value: str) -> float:
    match = re.search(r'(\d+(?:\.\d+)?)', value.replace(',', '.'))
    return float(match.group(1)) if match else 0.0


def parse_count_range(text: str) -> tuple[int, int]:
    text = text.strip()
    if '-' in text:
        parts = text.split('-', 1)
        try:
            return int(parts[0]), int(parts[1])
        except ValueError:
            pass
    if text.isdigit():
        n = int(text)
        return n, n
    return 0, 1
