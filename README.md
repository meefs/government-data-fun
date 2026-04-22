# OpenGovDash

A single-page browser app for exploring 21 US government agencies with ~56 data endpoints. Search, filter, cross-reference, and chat with an AI that can call the government APIs on your behalf.

**Live demo:** https://hbt89.github.io/government-data-fun/

## Features

- **21 agencies, ~56 endpoints.** SEC, FDA, Treasury, NOAA, NASA, USGS, BLS, Census, FDIC, NIH, FEC, LOC, USASpending, NIST, FCC, DOJ, DOT, EPA, SAM.gov, NARA, FTC — all fetched directly from the official APIs.
- **AI chat that actually calls the APIs.** Tool-use support for OpenAI, Groq, Anthropic Claude, and Google Gemini. A free HuggingFace fallback runs ReAct-style tool calls without a key.
- **Keys stay in your browser.** No server holds your API credentials. Masked display, inline validation, one-click revoke.
- **Zero build step.** Single HTML file, vanilla JS, runs from any static host.

## Run it

### Option 1 — use the live demo

Open https://hbt89.github.io/government-data-fun/ and follow the setup wizard.

### Option 2 — host it yourself on GitHub Pages

Fork the repo, push, and the included `deploy-pages.yml` workflow publishes `webapp/static/` automatically. Update the `PROXY_BASE` constant in `webapp/static/index.html` to point at your own Cloudflare Worker (see `proxy/`) if you want the CORS-restricted agencies (BLS, NIH, LOC, USAspending, DOJ, DOT, EPA, SAM, FTC, NARA) to work from the hosted site.

### Option 3 — run locally with the Flask backend (self-hoster)

The backend proxies the CORS-restricted agencies and provides an OpenAI chat endpoint.

```bash
cd webapp
pip install -r requirements.txt
python app.py
# http://localhost:5000
```

### Option 4 — static only, locally

```bash
cd webapp/static
python -m http.server 8000
# http://localhost:8000/index.html
```

## API keys

OpenGovDash works immediately in **Free mode** (HuggingFace serverless). For higher quality or tool-use, paste a key into the setup wizard:

| Provider | Free tier | Signup |
|---|---|---|
| Groq | Yes (14.4k req/day) | https://console.groq.com/keys |
| Google Gemini | Yes (1.5k req/day) | https://aistudio.google.com/app/apikey |
| Anthropic Claude | Pay-per-use | https://console.anthropic.com/settings/keys |
| OpenAI | Pay-per-use | https://platform.openai.com/api-keys |
| data.gov | Yes | https://api.data.gov/signup/ |

All keys live in your browser's `localStorage`. The site never transmits them anywhere except to the provider you entered them for.

## Architecture

```
government-data-fun/
├── webapp/
│   ├── static/index.html     # The entire frontend (single file, ~4k lines)
│   ├── app.py                # Optional Flask backend for self-hosters
│   ├── requirements.txt
│   └── api/agency_modules/   # One module per agency (21 total)
├── proxy/                    # Cloudflare Worker for CORS-restricted agencies
│   ├── worker.js
│   └── wrangler.toml
├── .github/workflows/        # deploy-pages, deploy-worker, smoke-test, lint
└── docs/
    ├── CHANGELOG.md
    └── archive/              # Historical design notes
```

Frontend strategy per agency:
1. Try direct browser fetch against the official API.
2. If CORS-blocked and you're on a static host, route through the Cloudflare Worker at `PROXY_BASE`.
3. If running locally with the Flask backend, fall back to `/api/data/<agency>` on the backend.

## AI chat tool-use

The chat exposes ~30 tools mapped one-to-one with the agency data layer (`search_sec_filings`, `search_pubmed`, `search_fcc_equipment`, `cross_reference`, etc.). Tool-use works on:

- OpenAI (native `tools`)
- Groq (OpenAI-compatible)
- Anthropic Claude (`tools` + `input_schema`)
- Google Gemini (`functionDeclarations`)
- HuggingFace Free (ReAct JSON fallback)

Example prompts:
- *"Which SEC 8-K filings from the last 30 days mention cybersecurity?"*
- *"Look up FCC ID 2ABCB-1234 and cross-reference with FDA 510(k)."*
- *"How do NIST CVEs connect to recent FTC enforcement actions?"*

## Contributing

Issues and PRs welcome. See `docs/archive/` for design context on prior fixes.

## License

MIT.
