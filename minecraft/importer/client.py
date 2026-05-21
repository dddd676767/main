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
