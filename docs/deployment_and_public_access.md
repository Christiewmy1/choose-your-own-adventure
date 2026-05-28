# Deployment And Public Access

## Public website

- URL: `https://christiewmy1.github.io/choose-your-own-adventure/`
- Deployment mechanism: GitHub Pages
- Workflow file: `.github/workflows/deploy-web.yml`
- Source app: `web/`

## Public API

- Target URL: `https://choose-your-own-adventure-bay.vercel.app`
- Deployment mechanism: Vercel
- Config file: `vercel.json`
- App entry: `api/main.py`

## Local development mirrors

### Local backend

```bash
cd /Users/matiyasdawit/Desktop/CSS_382_Sp_26/AI_Project
PYTHONPATH=src uvicorn api.main:app --host 127.0.0.1 --port 8010
```

### Local frontend

```bash
cd /Users/matiyasdawit/Desktop/CSS_382_Sp_26/AI_Project/web
npm install
npm run dev
```

## Frontend API targeting

The frontend now supports:

- local API by default when running on `localhost` or `127.0.0.1`
- deployed API by default when loaded from the public website

That behavior is implemented in:

- `web/src/api.ts`

## Security note

The public demo does not currently require password-protected access. No credentials are required in the README at this time.

## Deployment risks

- The static frontend can appear updated before GitHub Pages finishes cache invalidation.
- GitHub Pages caching can temporarily show stale website assets.
- If the public API is temporarily unavailable, the frontend now shows a clearly labeled demo-safe fallback instead of a broken result page.
- Browser-opened API POST routes can show 405 or 404 if visited directly; the public website calls them with POST requests.
