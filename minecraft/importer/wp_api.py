from importer.client import BASE_URL, WikiClient

WP_API = f'{BASE_URL}/wp-json/wp/v2'


def iter_posts(client: WikiClient, category_id: int | None = None, per_page: int = 100):
    page = 1
    while True:
        params = f'?per_page={per_page}&page={page}'
        if category_id is not None:
            params += f'&categories={category_id}'
        data = client.fetch_json(f'{WP_API}/posts{params}')
        if not data:
            break
        yield from data
        if len(data) < per_page:
            break
        page += 1


def iter_categories(client: WikiClient, per_page: int = 100):
    page = 1
    while True:
        data = client.fetch_json(f'{WP_API}/categories?per_page={per_page}&page={page}')
        if not data:
            break
        yield from data
        if len(data) < per_page:
            break
        page += 1
