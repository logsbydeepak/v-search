# Quickly Database Package

This package provides shared PostgreSQL helpers and the database schema for Quickly.

## Connection

`db.connect()` reads `DB_URL` unless a URL is passed directly:

```sh
export DB_URL="postgresql://user:password@localhost:5432/quickly"
```

`get_db()` returns a cached connection for scripts. `get_db(scope)` attaches the connection to a scope object, which the Flask API uses with `flask.g`.

## Schema

The schema creates:

- `quickly_page`: crawled page metadata and content.
- `quickly_robot`: cached `robots.txt` documents.
- `quickly_page_link`: page-to-page links.
- `quickly_word_index`: token frequencies by page.

Indexes are added for backlink lookups, created dates, indexed words, and page IDs.

## Commands

Initialize tables:

```sh
make init_db
```

Drop tables:

```sh
make drop_db
```

Both commands run through `main.py`, which executes the SQL in `schema.py`.
