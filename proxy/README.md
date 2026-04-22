# opengov-proxy — Cloudflare Worker

A tiny CORS-friendly pass-through for the ~10 US government APIs that don't send CORS headers. Used by the OpenGovDash static site so it can fetch BLS, PubMed, LOC, USASpending, DOJ, NHTSA, EPA, SAM, FTC, NARA, and FCC ECFS directly from a browser.

## Deploy

Automatic: push any change under `proxy/` to `main`. The `deploy-worker.yml` GitHub Actions workflow runs `wrangler deploy` using the `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID` repo secrets.

Manual:

```bash
cd proxy
npx wrangler deploy
```

After deploy, the Worker is reachable at:

```
https://opengov-proxy.<your-subdomain>.workers.dev
```

Find `<your-subdomain>` with:

```bash
npx wrangler whoami
```

…or from the Cloudflare dashboard → Workers & Pages → your-subdomain badge.

## URL shape

```
GET/POST https://opengov-proxy.<sub>.workers.dev/p/<slug>/<upstream-path>?<qs>
```

Where `<slug>` is one of:

| Slug | Upstream |
|---|---|
| `bls` | `https://api.bls.gov` |
| `nih_pubmed` | `https://eutils.ncbi.nlm.nih.gov` |
| `loc` | `https://www.loc.gov` |
| `usaspending` | `https://api.usaspending.gov` |
| `doj` | `https://www.justice.gov` |
| `dot` | `https://api.nhtsa.gov` |
| `epa` | `https://data.epa.gov` |
| `sam` | `https://api.sam.gov` |
| `ftc` | `https://reportportal.ftc.gov` |
| `nara` | `https://catalog.archives.gov` |
| `fcc_ecfs` | `https://publicapi.fcc.gov` |

`GET /health` returns `{ok: true, upstreams: [...]}` for uptime probes.

## Security notes

- `Access-Control-Allow-Origin` is pinned to `selvidge.tech`, `*.github.io`, and `localhost`. Other origins get `selvidge.tech` (their browsers will block the response).
- Inbound `Authorization`, `Cookie`, `X-Forwarded-For`, `X-Real-IP`, and `CF-*` headers are dropped before forwarding. The proxy never leaks client-side auth to the upstream gov API.
- The proxy never holds a secret. Agencies that need a key (SAM, data.gov-gated NASA/FEC endpoints) receive the user's key as a query string exactly as they would on a direct fetch.
- `Set-Cookie` is stripped from the response.

## Free-tier limits

Cloudflare Workers free plan: 100,000 requests/day, 10ms CPU time/request. OpenGovDash's usage pattern (~10 requests per pageview across the 10 proxied agencies) means the free tier covers ~10k pageviews/day, which is plenty for a public demo.
