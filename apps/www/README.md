# Quickly Web

This Astro app is the browser experience for Quickly. It provides a search home page, a server-rendered results page, shared theme handling, and client-side search form behavior.

## Pages

- `/` renders the large search entry page with random suggestion chips.
- `/search?q=term&page=1` fetches API results, renders pagination, related searches, quick facts, and outbound result links.

See [src/pages/README.md](src/pages/README.md) for page-level notes.

## Components And Assets

- `src/components/Logo.astro` renders the Quickly mark.
- `src/components/Footer.astro` renders the shared footer.
- `src/components/ThemeHead.astro` initializes the light/dark theme before the page paints.
- `src/scripts/quickly.js` powers search form submission, clearing, suggestions, random search, and theme toggling.
- `src/styles/global.css` contains Tailwind imports, theme variables, and animation helpers.
- `public/favicon.svg` and `public/favicon.ico` provide browser icons.

## Configuration

The frontend reads `PUBLIC_API_URL` to call the search API. If unset, local defaults are used in the pages:

```sh
export PUBLIC_API_URL="http://127.0.0.1:5000"
```

## Development

Install dependencies:

```sh
bun install
```

Run the dev server:

```sh
bun run dev
```

Build for production:

```sh
bun run build
```

Preview the production build:

```sh
bun run preview
```
