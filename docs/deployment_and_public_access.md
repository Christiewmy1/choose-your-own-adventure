# Deployment And Public Access

## Public website

- URL: `https://christiewmy1.github.io/choose-your-own-adventure/`
- Deployment mechanism: GitHub Pages
- Workflow file: `.github/workflows/deploy-web.yml`
- Source app: `web/`

## Public API

- Target URL: `https://huskyadvisor-api-matiyas.vercel.app`
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
- the deployed Vercel API by default when loaded from GitHub Pages
- relative `/api` and `/health` calls when the frontend is hosted on Vercel with `web/vercel.json` rewrites

That behavior is implemented in:

- `web/src/api.ts`

## Backend freshness check

The public `/health` endpoint should return:

- `status: ok`
- `api_contract: ai_trace_v1`
- `supported_major_pathways` of at least 6
- `course_records` of at least 120
- `company_records` of at least 140

If those fields are missing, the public backend is stale even if the health check returns HTTP 200.

## Security note

The public demo does not currently require password-protected access. No credentials are required in the README at this time.

## Deployment risks

- The static frontend can appear updated before GitHub Pages finishes cache invalidation.
- GitHub Pages caching can temporarily show stale website assets.
- If the public API is temporarily unavailable, the frontend now shows a clearly labeled demo-safe fallback instead of a broken result page.
- Browser-opened API POST routes can show 405 if visited directly; the public website calls them with POST requests.
- The public Vercel backend should be checked before presenting by confirming `/health` reports `api_contract: ai_trace_v1` and `company_records: 140`.

## Latest QA finding

The local code passed a 560-profile deep QA simulation and API contract tests. The refreshed public backend at `https://huskyadvisor-api-matiyas.vercel.app` reports the `ai_trace_v1` contract, 6 supported pathways, 128 course records, and 140 company records. A public `JPMorgan Chase Technology` profile recommendation also returns `ai_trace`, confirming that the expanded company dataset is active in production.
