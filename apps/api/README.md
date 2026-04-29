# Quickly API

This Flask app exposes the search endpoint used by the Astro frontend.

## Endpoint

### `GET /search`

Query parameters:

- `q`: search text. Empty values return an empty result set.
- `page`: 1-based page number. Defaults to `1`.
- `page_size`: results per page. Defaults to `10` and is capped at `50`.

Example:

```sh
curl "http://127.0.0.1:5000/search?q=python&page=1"
```

Response shape:

```json
{
  "results": [
    {
      "url": "https://example.com",
      "title": "Example",
      "description": "Short summary",
      "score": 12
    }
  ],
  "meta": {
    "query": "python",
    "search_speed_ms": 6.1,
    "total_results": 1
  },
  "pagination": {
    "page": 1,
    "page_size": 10,
    "total_pages": 1,
    "has_next": false,
    "has_previous": false
  }
}
```

## Ranking

The API tokenizes the query with `tkz`, finds matching rows in `quickly_word_index`, joins page metadata from `quickly_page`, counts backlinks from `quickly_page_link`, and sorts by:

1. Total score
2. Keyword score
3. Backlink count
4. Title

## Development

Set `DB_URL` first:

```sh
export DB_URL="postgresql://user:password@localhost:5432/quickly"
```

Run from the repository root:

```sh
make api
```

Or run directly inside this directory:

```sh
uv run flask --app main run
```

The app adds permissive CORS headers so the local Astro frontend can call it during development.
