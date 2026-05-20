# Minecraft Wiki API

Django REST API справочника Minecraft (предметы, мобы, биомы, рецепты, версии).

## Импорт данных

Данные загружаются с [idpredmetov.ru](https://idpredmetov.ru) management-командой.

### Установка зависимостей

```bash
pip install -r requirements.txt
playwright install chromium
```

### Миграции

```bash
python manage.py migrate
```

### Запуск импорта

```bash
# Полный импорт (долго: ~1900 страниц предметов)
python manage.py scrape_idpredmetov

# Тестовый прогон без записи в БД
python manage.py scrape_idpredmetov --dry-run --limit-items 5

# Продолжить с кэшем slug и пропуском существующих
python manage.py scrape_idpredmetov --skip-existing

# Без Rich UI (логи в консоль)
python manage.py scrape_idpredmetov --no-ui --delay 0.3
```

### Параметры

| Флаг | Описание |
|------|----------|
| `--dry-run` | Парсинг без записи в БД |
| `--skip-existing` | Не перезагружать уже импортированные сущности |
| `--delay 0.5` | Пауза между HTTP-запросами (сек) |
| `--limit-items N` | Ограничить число предметов |
| `--no-ui` | Отключить живую панель Rich |

### Что импортируется

1. Измерения и версии Minecraft
2. Биомы (`/biomy/`)
3. Предметы (WordPress API + HTML-страницы)
4. Мобы (`/id-mobov/` + карточки)
5. Лут с мобов
6. Структуры из статей версий
7. Рецепты (карточки предметов + `/recepty/` через Playwright)
8. Кумулятивная привязка `versions` (в каждой версии — весь контент из прошлых)

Кэш slug предметов: `importer/cache/item_slugs.json`

### Тесты парсеров

```bash
pytest importer/tests/ -v
```

### Источник данных

Контент принадлежит idpredmetov.ru. Используйте импорт только в образовательных/личных целях с уважением к robots.txt и разумной частотой запросов.
