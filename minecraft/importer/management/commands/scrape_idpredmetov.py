from django.core.management.base import BaseCommand
from rich.console import Console

from importer.services.upsert import run_import


class Command(BaseCommand):
    help = 'Импорт данных Minecraft с idpredmetov.ru в локальную БД'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Парсинг без записи в БД',
        )
        parser.add_argument(
            '--skip-existing',
            action='store_true',
            help='Пропускать уже существующие записи',
        )
        parser.add_argument(
            '--delay',
            type=float,
            default=0.5,
            help='Задержка между HTTP-запросами (сек)',
        )
        parser.add_argument(
            '--no-ui',
            action='store_true',
            help='Отключить Rich Live dashboard',
        )
        parser.add_argument(
            '--limit-items',
            type=int,
            default=None,
            help='Ограничить число предметов (для тестов)',
        )

    def handle(self, *args, **options):
        console = Console()
        console.print('[bold green]Старт импорта idpredmetov.ru[/]')
        stats = run_import(
            dry_run=options['dry_run'],
            skip_existing=options['skip_existing'],
            delay=options['delay'],
            no_ui=options['no_ui'],
            limit_items=options['limit_items'],
        )
        console.print()
        console.print('[bold]Итог:[/]')
        console.print(f'  Версии:     {stats.versions}')
        console.print(f'  Предметы:   {stats.items}')
        console.print(f'  Мобы:       {stats.mobs}')
        console.print(f'  Биомы:      {stats.biomes}')
        console.print(f'  Структуры:  {stats.structures}')
        console.print(f'  Рецепты:    {stats.recipes}')
        console.print(f'  Лут:        {stats.loot_drops}')
        console.print(f'  Ошибки:     {stats.errors}')
        console.print(f'  Пропущено:  {stats.skipped}')
        if options['dry_run']:
            console.print('[yellow]Режим dry-run — данные в БД не записывались[/]')
