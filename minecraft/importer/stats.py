from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Optional

from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.table import Table


@dataclass
class ScrapeStats:
    stage: str = 'init'
    stage_current: int = 0
    stage_total: int = 0
    current_url: str = ''
    versions: int = 0
    items: int = 0
    mobs: int = 0
    biomes: int = 0
    structures: int = 0
    recipes: int = 0
    loot_drops: int = 0
    dimensions: int = 0
    errors: int = 0
    skipped: int = 0
    _started: float = field(default_factory=time.monotonic)

    def render(self) -> Panel:
        table = Table.grid(padding=(0, 2))
        table.add_column(style='bold cyan')
        table.add_column()

        progress = ''
        if self.stage_total:
            progress = f' ({self.stage_current}/{self.stage_total})'
        table.add_row('Этап:', f'{self.stage}{progress}')
        if self.current_url:
            url = self.current_url
            if len(url) > 70:
                url = url[:67] + '...'
            table.add_row('URL:', url)

        counts = (
            f'Версии: {self.versions}  Предметы: {self.items}  Мобы: {self.mobs}  '
            f'Биомы: {self.biomes}  Структуры: {self.structures}  '
            f'Рецепты: {self.recipes}  Лут: {self.loot_drops}'
        )
        table.add_row('Счётчики:', counts)
        table.add_row('Ошибки:', str(self.errors))
        table.add_row('Пропущено:', str(self.skipped))

        elapsed = time.monotonic() - self._started
        if self.stage_current and self.stage_total and self.stage_current > 0:
            rate = self.stage_current / elapsed
            remaining = (self.stage_total - self.stage_current) / rate if rate else 0
            table.add_row('ETA:', f'{remaining:.0f} с')
        table.add_row('Время:', f'{elapsed:.0f} с')

        return Panel(table, title='Импорт idpredmetov.ru', border_style='green')

    def set_stage(self, stage: str, current: int = 0, total: int = 0):
        self.stage = stage
        self.stage_current = current
        self.stage_total = total


class StatsDisplay:
    def __init__(self, stats: ScrapeStats, enabled: bool = True):
        self.stats = stats
        self.enabled = enabled
        self._live: Optional[Live] = None

    def __enter__(self):
        if self.enabled:
            self._live = Live(
                self.stats.render(),
                console=Console(),
                refresh_per_second=4,
            )
            self._live.__enter__()
        return self

    def __exit__(self, *args):
        if self._live:
            self._live.update(self.stats.render())
            self._live.__exit__(*args)

    def refresh(self):
        if self._live:
            self._live.update(self.stats.render())

    def tick(self, url: str = '', current: Optional[int] = None):
        if url:
            self.stats.current_url = url
        if current is not None:
            self.stats.stage_current = current
        self.refresh()
