# Quickly Tokenizer

`tkz` is the shared tokenizer used by the indexer and API.

## Behavior

`tokenize(text)`:

- Lowercases the input.
- Extracts alphanumeric words with a regular expression.
- Removes English stop words from NLTK.
- Returns an empty list for empty input.

NLTK stop words are read from `/tmp/nltk_data`. If they are missing, the package downloads them there on first use.

## Example

```python
import tkz

tokens = tkz.tokenize("Search the web, fast.")
print(tokens)
```

## Used By

- `apps/index` to create `quickly_word_index` rows from crawled page content.
- `apps/api` to tokenize incoming search queries before looking up indexed pages.
