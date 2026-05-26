<<<<<<< HEAD
import hashlib
import re
import time
from pathlib import Path

import requests

BASE_URL = 'https://idpredmetov.ru'
USER_AGENT = 'MinecraftWikiImporter/1.0 (+local dev)'
CACHE_DIR = Path(__file__).resolve().parent / 'cache'


class WikiClient:
    def __init__(self, delay=1.0, use_cache=True, max_retries=3):
        self.session = requests.Session()
        self.session.headers['User-Agent'] = USER_AGENT
        self.delay = delay
        self.use_cache = use_cache
        self.max_retries = max_retries
        if use_cache:
            CACHE_DIR.mkdir(parents=True, exist_ok=True)

    def _cache_path(self, url: str, ext: str = 'html') -> Path:
        key = hashlib.md5(url.encode()).hexdigest()
        return CACHE_DIR / f'{key}.{ext}'

    def _request(self, url: str) -> requests.Response:
        last_error = None
        for attempt in range(self.max_retries):
            time.sleep(self.delay * (attempt + 1))
            try:
                response = self.session.get(url, timeout=60)
                if response.status_code == 429:
                    time.sleep(self.delay * (2 ** attempt) * 2)
                    continue
                response.raise_for_status()
                return response
            except requests.RequestException as exc:
                last_error = exc
                time.sleep(self.delay * (2 ** attempt))
        raise last_error  # type: ignore[misc]

    def fetch(self, path: str) -> str:
        url = path if path.startswith('http') else f'{BASE_URL}/{path.lstrip("/")}'
        cache_path = self._cache_path(url)
        if self.use_cache and cache_path.exists():
            return cache_path.read_text(encoding='utf-8', errors='replace')

        response = self._request(url)
        text = response.text
        if self.use_cache:
            cache_path.write_text(text, encoding='utf-8')
        return text

    def fetch_json(self, path: str):
        url = path if path.startswith('http') else f'{BASE_URL}/{path.lstrip("/")}'
        cache_path = self._cache_path(url, ext='json')
        if self.use_cache and cache_path.exists():
            import json
            return json.loads(cache_path.read_text(encoding='utf-8'))

        response = self._request(url)
        data = response.json()
        if self.use_cache:
            import json
            cache_path.write_text(json.dumps(data, ensure_ascii=False), encoding='utf-8')
        return data


GIVE_RE = re.compile(r'/give\s+@\w+\s+([\w:]+)')
MINECRAFT_ID_RE = re.compile(r'minecraft:([\w]+)')
TEXT_ID_RE = re.compile(r'текстовым ID\s+([\w]+)', re.I)
MOB_ID_RE = re.compile(r'ID\s+["\']?([\w]+)["\']?', re.I)
STRUCTURE_ID_RE = re.compile(r'ID\s+["\']([\w]+)["\']', re.I)
LOCATE_RE = re.compile(r'/locate\s+([\w]+)')
=======
import time
from typing import Optional

import requests
from bs4 import BeautifulSoup
from django.conf import settings
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

BASE_URL = getattr(settings, 'IMPORTER_BASE_URL', 'https://idpredmetov.ru')
USER_AGENT = (
    'MinecraftWikiImporter/1.0 (+https://github.com; educational; '
    'contact: local-dev)'
)


class ScrapeError(Exception):
    pass


class HttpClient:
    def __init__(self, delay: float = 0.5, session: Optional[requests.Session] = None):
        self.delay = delay
        self._last_request = 0.0
        self.session = session or requests.Session()
        self.session.headers.update({'User-Agent': USER_AGENT})

    def _throttle(self):
        elapsed = time.monotonic() - self._last_request
        if elapsed < self.delay:
            time.sleep(self.delay - elapsed)
        self._last_request = time.monotonic()

    @retry(
        retry=retry_if_exception_type((requests.RequestException, ScrapeError)),
        stop=stop_after_attempt(4),
        wait=wait_exponential(multiplier=1, min=2, max=30),
        reraise=True,
    )
    def get(self, path: str) -> str:
        url = path if path.startswith('http') else f'{BASE_URL.rstrip("/")}/{path.lstrip("/")}'
        self._throttle()
        response = self.session.get(url, timeout=60)
        if response.status_code == 429:
            time.sleep(10)
            raise ScrapeError(f'Rate limited: {url}')
        if response.status_code >= 500:
            raise ScrapeError(f'Server error {response.status_code}: {url}')
        response.raise_for_status()
        return response.text

    def get_json(self, path: str) -> dict | list:
        url = path if path.startswith('http') else f'{BASE_URL.rstrip("/")}/{path.lstrip("/")}'
        self._throttle()
        response = self.session.get(url, timeout=60)
        response.raise_for_status()
        return response.json()

    def get_soup(self, path: str) -> BeautifulSoup:
        return BeautifulSoup(self.get(path), 'lxml')

    def fetch_wp_posts(self, category_id: int, page: int = 1, per_page: int = 100) -> list:
        data = self.get_json(
            f'/wp-json/wp/v2/posts?categories={category_id}&per_page={per_page}&page={page}'
        )
        return data if isinstance(data, list) else []
>>>>>>> 846cf762af40ade9e079b9d382b3e18f8ab82502
