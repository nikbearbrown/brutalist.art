# One-time YouTube Data API setup for @MedhavyAI

`publish_playlist.py` uploads and manages playlists through the YouTube Data API v3.
That needs an OAuth credential tied to the Google account that owns **@MedhavyAI**.
This is a once-per-machine setup; after it, uploads are non-interactive.

## 1. Google Cloud project + API
1. Go to https://console.cloud.google.com/ signed in as the **@MedhavyAI owner**.
2. Create (or pick) a project.
3. **APIs & Services → Library → YouTube Data API v3 → Enable.**

## 2. OAuth consent screen
1. **APIs & Services → OAuth consent screen.**
2. User type **External**. Fill app name / support email.
3. **Add the @MedhavyAI Google account as a Test user.** (In "Testing" mode only test
   users can authorize — that's fine; it doesn't limit uploads.)
4. Scopes can be left default; the script requests upload + playlist scopes at run time.

## 3. OAuth client (Desktop app)
1. **APIs & Services → Credentials → Create Credentials → OAuth client ID.**
2. Application type **Desktop app**.
3. Download the JSON, save it next to where you'll run the script as **`client_secret.json`**.

## 4. First run mints the token
Run any real (non-`--dry-run`) command once, e.g.:
```bash
python scripts/publish_playlist.py --root path/to/notebooklm-videos --dry-run   # verifies auth
python scripts/publish_playlist.py --root path/to/notebooklm-videos             # first real run
```
A browser opens; sign in as **@MedhavyAI** and approve. The script writes
**`youtube_token.json`** and reuses it silently afterward (auto-refreshing).

Keep `client_secret.json` and `youtube_token.json` private — they are channel credentials.
Point at them explicitly with `--client` / `--token` if they live elsewhere.

## 5. Public vs unlisted — the audit
Uploads via the API are capped at **unlisted/private** until Google approves an **API
compliance audit** for the project. Until then:
- Post as `unlisted` (default) and flip each to Public in YouTube Studio by hand, **or**
- Request the audit (APIs & Services → your project) and then use `--privacy public`.

## Quota
Each upload costs ~1600 quota units; the default daily quota (10,000) is roughly **6
uploads/day**. For a full volume, spread uploads across days or request more quota. The
script keeps a `publish_ledger.json`, so re-running after hitting the cap just resumes —
already-uploaded videos are skipped.
