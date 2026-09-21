# FIX: YouTube publisher posts to wrong Google account

## Root cause

`get_service()` in `publish_playlist.py` caches the OAuth token in
`youtube/credentials/<channel>/youtube_token.json`. When a browser session
is already logged into a different Google account, the OAuth consent screen
silently mints the token for that account — not the one the `--channel` flag
names. The script never checks which channel it actually authenticated as
before uploading.

## Two-part fix — edit `publish_playlist.py`

File: `brutalist-art/skills/upload/youtube-publisher/scripts/publish_playlist.py`

---

### Fix 1 — force account-picker on every new OAuth flow (line 115)

Old:
```python
creds = flow.run_local_server(port=0)
```

New:
```python
creds = flow.run_local_server(port=0, prompt="select_account")
```

This passes `prompt=select_account` through to the Google authorization URL,
so the browser always shows the account chooser instead of defaulting to the
currently-logged-in session.

---

### Fix 2 — print authenticated channel immediately after auth

Add this function directly after the `get_service()` definition (before
`find_or_create_playlist`):

```python
def verify_authenticated_channel(youtube, expected_id: str = "") -> str:
    """Print the authenticated channel name/ID; abort if it doesn't match expected_id."""
    resp = youtube.channels().list(part="snippet", mine=True, maxResults=1).execute()
    items = resp.get("items", [])
    if not items:
        print("[yt] WARNING: could not read authenticated channel — no channel linked to this account?")
        return ""
    name = items[0]["snippet"]["title"]
    cid  = items[0]["id"]
    print(f"[yt] authenticated as: {name}  (channel ID: {cid})")
    if expected_id and cid != expected_id:
        raise SystemExit(
            f"[yt] ABORT — wrong account.\n"
            f"    Expected channel ID : {expected_id}\n"
            f"    Got                 : {cid} ({name})\n"
            f"    Delete youtube_token.json and re-run to pick the correct account."
        )
    return cid
```

Then in `main()`, call it immediately after `get_service()` (around line 301):

Old:
```python
youtube = get_service(client_p, token_p)
playlist_id = find_or_create_playlist(...)
```

New:
```python
youtube = get_service(client_p, token_p)
_expected = ""
_eid_file = _cred / "expected_channel_id.txt"
if _eid_file.exists():
    _expected = _eid_file.read_text().strip()
verify_authenticated_channel(youtube, expected_id=_expected)
playlist_id = find_or_create_playlist(...)
```

---

### Fix 3 — write expected_channel_id.txt for each channel folder

After running the publisher once with the correct account, grab the printed
channel ID and save it:

```bash
# humanitarians
echo "UC<the-channel-id-printed-above>" \
  > brutalist-art/youtube/credentials/humanitarians/expected_channel_id.txt

# nikbearbrown
echo "UC<the-channel-id>" \
  > brutalist-art/youtube/credentials/nikbearbrown/expected_channel_id.txt

# musinique (when token exists)
echo "UC<the-channel-id>" \
  > brutalist-art/youtube/credentials/musinique/expected_channel_id.txt
```

These files are already gitignored (they sit beside `youtube_token.json`).
Once written, any future run against the wrong account aborts with a clear
message before touching YouTube.

---

## How to test the fix without uploading

```bash
python3 brutalist-art/skills/upload/youtube-publisher/scripts/publish_playlist.py \
  brutalist-art/youtube/claude-liam-hai-how-to-explainer-videos \
  --playlist "Humanitarians AI Fellows" \
  --channel humanitarians \
  --privacy unlisted \
  --no-anchor \
  --dry-run
```

`--dry-run` authenticates but does not upload. Check the printed line:

```
[yt] authenticated as: Humanitarians AI  (channel ID: UC...)
```

If it says NikBearBrown or anything else, delete
`brutalist-art/youtube/credentials/humanitarians/youtube_token.json` and
re-run — the browser will ask you to pick an account (Fix 1 forces the picker).
