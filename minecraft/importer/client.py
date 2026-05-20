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
