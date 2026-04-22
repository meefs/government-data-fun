# Changelog

## Unreleased

### Added
- Root `.gitignore` covering Python, Node, Cloudflare Worker, and editor artifacts.
- `.env.example` documenting optional self-hoster backend variables.
- `.github/workflows/deploy-pages.yml` — automatic static deploy from `main` via `actions/deploy-pages`.
- `docs/archive/` — archived prior internal notes (API_STATUS, API_FAILURES_ANALYSIS, CHAT_UX_FIXES, FIXES_APPLIED, IMPLEMENTATION_COMPLETE).

### Removed
- Legacy `app.py` at repo root (superseded by modular `webapp/app.py`).

### Changed
- `README.md` top section rewritten for the GitHub Pages deployment model.
