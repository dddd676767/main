from django.core.management.base import BaseCommand

from importer.client import WikiClient
from importer.loaders import ImportStats, WikiImporter

SECTIONS = ('biomes', 'effects', 'enchantments', 'structures', 'items', 'mobs', 'recipes')


class Command(BaseCommand):
    help = 'Import Minecraft wiki data from idpredmetov.ru into the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--only',
            choices=SECTIONS,
            action='append',
            help='Import only specific sections (can repeat)',
        )
        parser.add_argument('--deep', action='store_true', help='Fetch detail pages for items, mobs, recipes')
        parser.add_argument('--dry-run', action='store_true', help='Parse without writing to DB')
        parser.add_argument('--no-cache', action='store_true', help='Disable HTML cache')
        parser.add_argument('--delay', type=float, default=1.0, help='Delay between HTTP requests (seconds)')

    def handle(self, *args, **options):
        only = options['only'] or list(SECTIONS)
        client = WikiClient(delay=options['delay'], use_cache=not options['no_cache'])
        importer = WikiImporter(client, dry_run=options['dry_run'], deep=options['deep'])

        total = ImportStats()
        self.stdout.write('Seeding dimensions and version...')
        total.merge(importer.seed())
        if not options['dry_run']:
            from dimensions.models import Dimension
            from versions.models import MinecraftVersion
            importer.dimensions = {d.name: d for d in Dimension.objects.all()}
            importer.version = MinecraftVersion.objects.filter(is_latest=True).first()

        runners = {
            'biomes': importer.import_biomes,
            'effects': importer.import_effects,
            'enchantments': importer.import_enchantments,
            'structures': importer.import_structures,
            'items': importer.import_items,
            'mobs': importer.import_mobs,
            'recipes': importer.import_recipes,
        }

        for section in only:
            if section == 'recipes' and not options['deep']:
                self.stdout.write(self.style.WARNING(
                    'Recipes require --deep (detail page parsing). Skipping recipes.'
                ))
                continue
            if section == 'mobs' and 'items' not in only and section in only:
                importer._refresh_item_lookup()
            if section == 'recipes':
                importer._refresh_item_lookup()
            self.stdout.write(f'Importing {section}...')
            stats = runners[section]()
            total.merge(stats)
            self._print_stats(section, stats)

        self.stdout.write(self.style.SUCCESS('\n=== Total ==='))
        self._print_stats('all', total)

    def _print_stats(self, label: str, stats: ImportStats):
        self.stdout.write(
            f'  [{label}] created={stats.created} updated={stats.updated} '
            f'skipped={stats.skipped} errors={len(stats.errors)}'
        )
        for err in stats.errors[:20]:
            self.stdout.write(self.style.ERROR(f'    {err}'))
        if len(stats.errors) > 20:
            self.stdout.write(self.style.ERROR(f'    ... and {len(stats.errors) - 20} more'))
