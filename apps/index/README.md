# Quickly Indexer

The indexer converts crawled pages into searchable word-frequency rows. It reads pages from `quickly_page`, tokenizes title, description, and content, then writes weighted terms into `quickly_word_index`.

## Weighting

- Title words add `5` points each.
- Description words add `3` points each.
- Body content words add `1` point each.

The API later combines these keyword frequencies with backlink counts to rank results.

## Running

Set `DB_URL` first:

```sh
export DB_URL="postgresql://user:password@localhost:5432/quickly"
```

Index all pages that do not already have word-index rows:

```sh
make index_all
```

Or call the module directly:

```sh
uv run python -c "import main; main.index_all_pages()"
```

## Notes

`index_all_pages` works in batches and skips pages that already exist in `quickly_word_index`. If page content changes and needs to be indexed again, clear the relevant rows from `quickly_word_index` before rerunning.
