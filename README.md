# OpenGovDash - Government Data Research Terminal

A lightning-fast, zero-setup web app for exploring 21 government agencies with 53+ data endpoints. Search, filter, and cross-reference with an AI chatbot that learns your data context.

## Features

**Data Access**
- 21 government agencies: SEC, FDA, Treasury, NOAA, NASA, USGS, BLS, Census, FDIC, NIH, FEC, LOC, USASpending, NIST, FCC, and more
- 53+ REST API endpoints with direct client-side access (no backend required)
- Real-time search and filtering
- Configurable fetch limits and date range controls
- Multi-format data views (cards, table)

**AI Chatbot**
- Multi-provider support: Free mode (HuggingFace), OpenAI, Groq, Google Gemini, Anthropic Claude
- Automatic API state detection — knows which providers are configured
- Context-aware responses using live government data
- Cross-agency relationship discovery

**User Experience**
- Terminal-style monospace aesthetic (zero border-radius, sharp UI)
- SVG icon system (45+ minimalist icons)
- Stateful API management with guided setup wizards
- Optional Flask backend proxy for CORS handling
- Responsive sidebar with agency navigation and endpoint badges

---

## Quick Start

![welcome](/images/Welcome.png)
### Option 1: Direct Browser (No Installation)
```bash
# Clone repo
git clone <repo-url>
cd government-data-fun/webapp

# Open in browser
open static/index.html
# or just drag the file to your browser
```

### Option 2: Local Server (Recommended for Stability)
```bash
cd government-data-fun/webapp/static
python3 -m http.server 8000
# Visit http://localhost:8000/index.html
```

### Option 3: With Flask Backend (Optional CORS Proxy)
```bash
cd government-data-fun
python3 app.py
# Backend runs on http://localhost:5000
# Frontend auto-detects and uses it for API proxying
```

---

## API Key Setup (Optional but Recommended)

The app works immediately with **Free Mode** — no keys needed. For other providers:

**On Welcome Page:**
- Quick setup grid for OpenAI, Groq, Google Gemini
- Click "Add" next to any provider
- Follow guided steps with direct links to provider consoles
- Paste API key into modal
- Status badges show what's configured

**Providers & Free Tiers:**
- **Free Mode** – HuggingFace open-source models (no key needed, rate-limited)
- **Google Gemini** – 60 req/min free, no credit card required ([get key](https://aistudio.google.com/app/apikey))
- **Groq** – Free tier available, very fast ([get key](https://console.groq.com/keys))
- **OpenAI** – Pay-per-use GPT-4o-mini ([get key](https://platform.openai.com/api-keys))
- **Anthropic Claude** – Pay-per-use Claude Sonnet ([get key](https://console.anthropic.com/api))

**data.gov API Key (Optional):**
- Some agencies offer better access with [data.gov key](https://api.data.gov/signup/) — totally optional

---

## How to Use

### Browse Data
![Data Cards](/images/NIHTables.png)
1. **Select an agency** from the left sidebar (SEC, FDA, NASA, etc.)
2. **Click endpoint card** to see what data is available (e.g., "SEC Filings", "FDA Drug Events")
3. **Search** for specific terms, companies, or identifiers
4. **Set limits** – choose 10/20/50/100 records to fetch
5. **Filter by date** – optional date range controls

### AI Chatbot
![Chat](/images/AIChat.png)
1. Click **"AI Cross-Reference Chatbot"** in the sidebar
2. **Free Mode works immediately** — no setup needed
3. Type questions like:
   - "What SEC filings relate to FDA drug approvals?"
   - "How do NIST CVEs connect to FTC enforcement?"
   - "Show relationships between Treasury data and FDIC banks"
4. The chatbot sees your live data context and answers with connections

### Configure More Providers
1. Click **"API Key"** button in chat topbar
2. Select provider and follow setup steps
3. Paste your key → "Save Key"
4. Status badges at top show what's active

---

## Architecture

**Single-File Frontend** (`webapp/static/index.html`)
- ~3500 lines HTML/CSS/JS
- No build step, no Node.js required
- Monospace terminal aesthetic with SVG icons
- Responsive sidebar + main content area

**API Integration**
- Direct fetch from government APIs (client-side)
- Falls back to Flask backend if CORS issues
- 21 agency modules with custom parsers per API format

**AI Chatbot**
- Integrates message history with live data context
- Supports multiple providers via their official APIs
- Free mode uses HuggingFace serverless inference

**State Management**
- `apiState` object tracks provider readiness
- Proactive setup guidance (Streamlit-style)
- Welcome wizard lets users configure up to 3 providers at setup

---

## Development

**Project Structure**
```
government-data-fun/
├── webapp/
│   ├── static/
│   │   └── index.html           # Complete single-file app
│   └── ...
├── app.py                        # Optional Flask backend
├── README.md
└── ...
```

**Making Changes**
1. Edit `webapp/static/index.html` directly
2. Refresh browser to test
3. No build or compilation needed

**Adding Agencies**
- Add agency config to `CLIENT_AGENCIES` in HTML
- Implement fetch function in `DIRECT_API` object
- Add SVG icon to `epIcons` map

---

## Troubleshooting

**Q: "Free mode error"**
A: Free mode uses HuggingFace models which occasionally get rate-limited. Refresh and retry, or add your own API key for a paid provider (more reliable).

**Q: Backend not connecting**
A: The app detects this automatically and switches to client-side mode. If you want CORS proxying, start the Flask backend: `python3 app.py`

**Q: Data not loading**
A: Some agencies require authentication or have rate limits. Check browser console (F12) for specific API error. Try different agency or adjust fetch limit.

**Q: API key modal keeps showing**
A: Make sure you actually clicked "Save Key" — the modal dismisses only after successful save. Check that your key doesn't have extra spaces.

---

## Tech Stack

- **Frontend**: Vanilla JS (no frameworks)
- **Styling**: CSS variables, monospace fonts, zero border-radius aesthetic
- **APIs**: Direct fetch + optional Flask proxy
- **AI**: HuggingFace, OpenAI, Groq, Google Gemini, Anthropic Claude
- **Icons**: Inline SVG (45+ minimalist icons)

---

## Agencies & Endpoints

**21 Agencies, 53+ Endpoints:**

| Agency | Key Endpoints |
|--------|---------------|
| SEC | Company filings (8-K, 10-K, 10-Q), company search |
| FDA | Drug events, device recalls, 510(k) approvals |
| Treasury | National debt, daily statements |
| NOAA | Earthquakes, tsunamis |
| NASA | APOD, asteroid tracking |
| USGS | Earthquake data, water resources |
| BLS | Employment statistics |
| Census | Demographic data |
| FDIC | Bank failures, financial institutions |
| NIH | PubMed articles, clinical trials |
| FEC | Campaign finance, donations |
| Library of Congress | Collections search |
| USASpending | Federal contracts and spending |
| NIST | Cybersecurity advisories |
| FCC | Equipment authorizations, ECFS filings, broadband data |
| And more... | Data varies by agency |

---

## Performance Notes

- **Cold start**: ~2-3 seconds (first API call)
- **Subsequent queries**: <500ms (browser-cached)
- **Data fetching**: Configurable limits (10-100 records per fetch)
- **AI responses**: 5-15 seconds depending on provider

---

## Future Enhancements

- [ ] Dashboard builder using live data
- [ ] Export to CSV/PDF
- [ ] Saved searches & favorites
- [ ] API webhook integration
- [ ] Rate limiting display
- [ ] Historical data trending

---

## Contributing

Found a bug or want to add an agency?
- Report issues with clear steps to reproduce
- Submit PRs with agency additions or feature improvements
- Check the code comments for integration points

---

## License
MIT License — Use freely in personal and commercial projects.
