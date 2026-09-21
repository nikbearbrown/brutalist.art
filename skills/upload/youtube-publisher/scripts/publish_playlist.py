#!/usr/bin/env python3
"""
publish_playlist.py — upload finished Medhavy videos to @MedhavyAI and add them to a
named playlist IN CHAPTER ORDER.

For each video folder (one per NotebookLM video, each with beat_sheet.json,
mp4/<slug>.mp4, and description.txt), this:
  1. authenticates to the YouTube Data API (OAuth desktop flow, cached token),
  2. finds — or creates — the target playlist by title,
  3. uploads any folder not already in the ledger, then
  4. inserts each into the playlist at the position given by its chapter_number,
     so the playlist reads in chapter order regardless of upload order, and
  5. uploads <slug>.srt as an English caption track (CC data) when present —
     idempotent (skips if the video already has a track), best-effort (a caption
     failure never blocks the upload or playlist), disable with --no-captions.

Videos upload as `unlisted` by default: a brand-new YouTube API project cannot make
uploads public until Google approves an API audit, and forcing `public` before that
just fails. Flip to --privacy public once audited (or publish each from the Studio UI).

One-time setup (see references/youtube-setup.md): a Google Cloud project with the
YouTube Data API enabled, an OAuth "Desktop app" client saved as client_secret.json,
and the @MedhavyAI account added as a test user on the consent screen.

Install:  pip install google-api-python-client google-auth-oauthlib google-auth-httplib2

Usage:
    # preview only — no upload, no quota:
    python publish_playlist.py --root path/to/notebooklm-videos --dry-run

    # upload everything not yet posted, add to the playlist in chapter order:
    python publish_playlist.py --root path/to/notebooklm-videos \
        --playlist "Quantum Mechanics Volume 1 (NotebookLM)"

    # specific folders:
    python publish_playlist.py FOLDER_A FOLDER_B --privacy public
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import os, json
import subprocess
import sys
import time
from pathlib import Path

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube",
    "https://www.googleapis.com/auth/youtube.force-ssl",  # captions.insert
]
EDU_CATEGORY = "27"

# ── TOPOST — the ONLY legal upload source ────────────────────────────────────
# Override ART_TOPOST in .env if the repo lives elsewhere, but the path must
# still resolve to the real TOPOST staging directory.
TOPOST = Path(os.environ.get(
    "ART_TOPOST",
    "/Users/bear/Documents/CoWork/bear-textbooks/books/youtube/TOPOST",
))
STAGED_JSON = TOPOST / "staged.json"


def _staged_find(staged: dict, name: str, stem: str) -> dict | None:
    """Find an entry in staged.json regardless of whether it uses the old
    dict-keyed format {"slug.mp4": {...}} or the new array format {"videos": [...]}.
    Returns the entry dict or None."""
    # New format: {"videos": [{slug, files.master_4k, ...}, ...]}
    if "videos" in staged and isinstance(staged["videos"], list):
        for v in staged["videos"]:
            master = v.get("files", {}).get("master_4k", "")
            if (v.get("slug") == stem
                    or v.get("slug") == name
                    or master == name
                    or Path(master).stem == stem):
                return v
    # Old format: {"slug.mp4": {...}, "slug": {...}}
    return staged.get(name) or staged.get(stem)


def _staged_set_uploaded(staged: dict, name: str, stem: str, video_id: str) -> None:
    """Mutate the matching entry in staged (either format) to status='uploaded'."""
    if "videos" in staged and isinstance(staged["videos"], list):
        for v in staged["videos"]:
            master = v.get("files", {}).get("master_4k", "")
            if (v.get("slug") == stem or v.get("slug") == name
                    or master == name or Path(master).stem == stem):
                v["status"] = "uploaded"
                v["video_id"] = video_id
                v["uploaded_at"] = datetime.datetime.utcnow().isoformat() + "Z"
                return
    # Old format
    key = name if name in staged else stem if stem in staged else None
    if key:
        staged[key]["status"] = "uploaded"
        staged[key]["video_id"] = video_id
        staged[key]["uploaded_at"] = datetime.datetime.utcnow().isoformat() + "Z"


def topost_preflight(video_path: Path) -> dict:
    """HARD preflight — three checks, no bypass flag.

    Call this immediately before any YouTube Data API upload call.
    Prints which check failed and the offending path, then sys.exit(1).
    Returns the staged.json entry dict on success.
    """
    real = Path(os.path.realpath(video_path))
    real_topost = Path(os.path.realpath(TOPOST))

    # ── Check 1: realpath inside TOPOST (symlinks cannot dodge this) ──────────
    try:
        real.relative_to(real_topost)
    except ValueError:
        print("[TOPOST GATE] FAIL — check 1: video is not inside TOPOST/")
        print(f"  offending path : {real}")
        print(f"  required inside: {real_topost}")
        print("  Run the 'post' skill to stage a hi-res master before publishing.")
        sys.exit(1)

    # ── Check 2: staged.json entry exists and status != 'uploaded' ────────────
    if not STAGED_JSON.exists():
        print("[TOPOST GATE] FAIL — check 2: staged.json not found")
        print(f"  expected: {STAGED_JSON}")
        print("  No video has been staged yet (run the 'post' skill first).")
        sys.exit(1)

    staged = json.loads(STAGED_JSON.read_text())
    name = real.name
    stem = real.stem
    entry = _staged_find(staged, name, stem)
    if not entry:
        print("[TOPOST GATE] FAIL — check 2: no staged.json entry for this file")
        print(f"  offending path: {real}")
        print(f"  staged.json   : {STAGED_JSON}")
        print("  Run the 'post' skill to register this file before publishing.")
        sys.exit(1)

    if entry.get("status") == "uploaded":
        print("[TOPOST GATE] FAIL — check 2: already marked 'uploaded' in staged.json")
        print(f"  offending path: {real}")
        print(f"  uploaded_at   : {entry.get('uploaded_at', 'n/a')}")
        print(f"  video_id      : {entry.get('video_id', 'n/a')}")
        sys.exit(1)

    # ── Check 3: ffprobe height >= 2160 (hi-res master only) ─────────────────
    try:
        probe = subprocess.run(
            ["ffprobe", "-v", "quiet", "-print_format", "json",
             "-show_streams", str(real)],
            capture_output=True, text=True, check=True,
        )
        streams = json.loads(probe.stdout).get("streams", [])
        height = next(
            (s["height"] for s in streams if s.get("codec_type") == "video"), 0
        )
    except Exception as exc:
        print("[TOPOST GATE] FAIL — check 3: ffprobe error")
        print(f"  offending path: {real}")
        print(f"  error         : {exc}")
        sys.exit(1)

    if height < 2160:
        print("[TOPOST GATE] FAIL — check 3: video is not hi-res (need height >= 2160)")
        print(f"  offending path: {real}")
        print(f"  measured height: {height}px")
        print("  Use the Topaz-upscaled 4K master from TOPOST, not a preview cut.")
        sys.exit(1)

    print(f"[TOPOST GATE] PASS — {name}  ({height}p · staged · not yet uploaded)")
    return entry


def update_staged_status(video_path: Path, video_id: str) -> None:
    """Flip the staged.json entry to status='uploaded' after a successful upload.

    Additive write: only touches the matching entry; all other entries are
    preserved exactly as-is.
    """
    real = Path(os.path.realpath(video_path))
    if not STAGED_JSON.exists():
        print(f"[TOPOST] WARNING: staged.json not found — upload status not recorded")
        return
    staged = json.loads(STAGED_JSON.read_text())
    name, stem = real.name, real.stem
    if not _staged_find(staged, name, stem):
        print(f"[TOPOST] WARNING: no staged.json entry for '{name}' — status not updated")
        return
    _staged_set_uploaded(staged, name, stem, video_id)
    STAGED_JSON.write_text(json.dumps(staged, indent=2))
    print(f"[TOPOST] staged.json: {name}  →  status=uploaded  video_id={video_id}")

# captions.insert intermittently 403s on freshly-uploaded videos until YouTube
# finishes processing them — this backoff covers ~14.5 min. Already-live videos
# get a single attempt (no waits).
FRESH_CAPTION_WAITS = [20, 40, 60, 90, 120, 180, 180, 180]

# ── Series anchors ───────────────────────────────────────────────────────────
# The whole series funnels to one intro video and one master playlist. By DEFAULT
# every SHORT's description points to the intro VIDEO ("What is Brutalist?"), and
# every LONG's description points to the series PLAYLIST ("Brutalist"). Override
# either in .env (blank disables that anchor); pass --no-anchor to skip entirely.
ANCHOR_VIDEO_URL    = os.environ.get("ART_ANCHOR_VIDEO_URL",
                                     "https://youtu.be/xXKgCXc1nm4")                       # What is Brutalist?
ANCHOR_PLAYLIST_URL = os.environ.get("ART_ANCHOR_PLAYLIST_URL",
                                     "https://www.youtube.com/playlist?list=PLG9H-C6rp5RU")  # Brutalist

def anchor_block(kind: str, parent_url: str = "", parent_title: str = "") -> str:
    if kind == "short":
        # THE FUNNEL: a short exists to send people to its 16:9 long. A derived
        # short (metadata.derived_from) anchors to its PARENT LONG; a standalone
        # short falls back to the series intro video.
        if parent_url:
            return (f"\n\n▶ Watch the full video — {parent_title or 'the long'}"
                    f"\n{parent_url}")
        return f"\n\n▶ Start the series — What is Brutalist?\n{ANCHOR_VIDEO_URL}" if ANCHOR_VIDEO_URL else ""
    return f"\n\n▶ The full series playlist — Brutalist\n{ANCHOR_PLAYLIST_URL}" if ANCHOR_PLAYLIST_URL else ""

def folder_kind(folder: Path, default: str) -> str:
    """A short if it lives in a short/ subfolder or its metadata says so; else the CLI default."""
    if folder.name == "short":
        return "short"
    try:
        m = json.loads((folder / "beat_sheet.json").read_text()).get("metadata", {})
    except Exception:
        m = {}
    if str(m.get("kind", "")).lower() == "short" or str(m.get("format", "")).lower() in ("short", "9:16", "vertical"):
        return "short"
    return default


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _pre_upload_assert(video_path: Path, staged_entry: dict, ledger: dict) -> None:
    """Hard pre-upload assertions (no bypass flag).

    Runs AFTER topost_preflight() (which already checked TOPOST path, staged.json
    existence, and height). This adds:
      4. sha256 file integrity: re-hash the file and match staged.json's sha256
         if one was recorded. If the entry has no sha256 (staged before Phase 3),
         emit a warning and continue — the absence is not a failure, but a mis-match is.
      5. Duplicate-upload guard: the sha256 must not already appear in the ledger's
         _uploaded_sha256s set (catches renamed files being re-uploaded).
      6. Companion files: <slug>.srt and <slug>.md must exist beside the master in TOPOST.

    Prints which check failed and calls sys.exit(1) on any hard failure.
    """
    real = Path(os.path.realpath(video_path))
    real_topost = Path(os.path.realpath(TOPOST))
    slug = real.stem

    # ── Check 4: sha256 integrity ─────────────────────────────────────────────
    recorded_sha256 = staged_entry.get("sha256", "")
    if recorded_sha256:
        actual_sha256 = _sha256_file(real)
        if actual_sha256 != recorded_sha256:
            print("[PRE-UPLOAD ASSERT] FAIL — check 4: sha256 mismatch (tamper/wrong-file guard)")
            print(f"  file          : {real}")
            print(f"  staged sha256 : {recorded_sha256[:16]}…")
            print(f"  actual sha256 : {actual_sha256[:16]}…")
            print("  The file was modified or replaced after staging. Re-run 'art post' to re-stage.")
            sys.exit(1)
        current_sha256 = actual_sha256
        print(f"[PRE-UPLOAD ASSERT] sha256 integrity: MATCH ✓  ({current_sha256[:16]}…)")
    else:
        # No sha256 in staged.json — this entry predates Phase 3 hardening.
        # Compute the hash for the duplicate check below but do not fail.
        current_sha256 = _sha256_file(real)
        print(f"[PRE-UPLOAD ASSERT] sha256: no recorded hash in staged.json "
              f"(pre-Phase3 entry) — computed {current_sha256[:16]}… for duplicate check")

    # ── Check 5: duplicate-upload guard ──────────────────────────────────────
    uploaded_hashes: list = ledger.get("_uploaded_sha256s", [])
    if current_sha256 in uploaded_hashes:
        print("[PRE-UPLOAD ASSERT] FAIL — check 5: sha256 already in upload ledger")
        print(f"  sha256  : {current_sha256[:16]}…")
        print(f"  file    : {real}")
        print("  This exact file content was already uploaded. Check the ledger for the video ID.")
        print("  If this is intentional (e.g. re-upload after deletion), remove the sha256 from")
        print("  the ledger's _uploaded_sha256s list manually.")
        sys.exit(1)

    # ── Check 6: companion files (.srt and .md) ───────────────────────────────
    srt = real_topost / f"{slug}.srt"
    md  = real_topost / f"{slug}.md"
    missing = []
    if not srt.exists():
        missing.append(f"{slug}.srt (run stage_publish.py to generate captions, then re-stage)")
    if not md.exists():
        missing.append(f"{slug}.md (run 'art post' to generate the description)")
    if missing:
        print("[PRE-UPLOAD ASSERT] FAIL — check 6: companion files missing from TOPOST")
        for m in missing:
            print(f"  missing: {m}")
        sys.exit(1)

    print(f"[PRE-UPLOAD ASSERT] companion files: {slug}.srt + {slug}.md ✓")


def get_service(client_secret: Path, token_path: Path):
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build

    creds = None
    if token_path.exists():
        # A token minted before a scope was added (e.g. force-ssl for captions)
        # would 403 on the new calls — force a fresh consent flow instead.
        info = json.loads(token_path.read_text())
        if set(SCOPES) - set(info.get("scopes") or []):
            print("[yt] cached token is missing newly-required scope(s) — re-running OAuth consent")
        else:
            creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not client_secret.exists():
                sys.exit(f"[yt] missing OAuth client secret: {client_secret}\n"
                         f"    See references/youtube-setup.md.")
            flow = InstalledAppFlow.from_client_secrets_file(str(client_secret), SCOPES)
            creds = flow.run_local_server(port=0, prompt="select_account")
        token_path.write_text(creds.to_json())
    return build("youtube", "v3", credentials=creds)


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


def find_or_create_playlist(youtube, title: str, privacy: str, dry: bool) -> str | None:
    req = youtube.playlists().list(part="id,snippet", mine=True, maxResults=50)
    while req is not None:
        resp = req.execute()
        for it in resp.get("items", []):
            if it["snippet"]["title"].strip().lower() == title.strip().lower():
                print(f"[yt] found playlist '{title}' → {it['id']}")
                return it["id"]
        req = youtube.playlists().list_next(req, resp)
    if dry:
        print(f"[yt] (dry-run) would CREATE playlist '{title}'")
        return None
    resp = youtube.playlists().insert(
        part="snippet,status",
        body={"snippet": {"title": title,
                          "description": "NotebookLM deep dives, chapter by chapter. By Medhavy."},
              "status": {"privacyStatus": "public" if privacy == "public" else "unlisted"}},
    ).execute()
    print(f"[yt] created playlist '{title}' → {resp['id']}")
    return resp["id"]


def already_in_playlist(youtube, playlist_id: str) -> dict:
    """videoId -> playlistItemId, so re-runs don't double-add."""
    import time
    from googleapiclient.errors import HttpError
    out = {}
    req = youtube.playlistItems().list(part="id,contentDetails", playlistId=playlist_id, maxResults=50)
    while req is not None:
        try:
            resp = req.execute()
        except HttpError as e:
            if e.resp.status == 404:
                # Newly created playlist not yet propagated — treat as empty
                time.sleep(3)
                return {}
            raise
        for it in resp.get("items", []):
            out[it["contentDetails"]["videoId"]] = it["id"]
        req = youtube.playlistItems().list_next(req, resp)
    return out


def has_caption_track(youtube, video_id: str) -> bool:
    """True if the video already has any caption track (re-runs stay idempotent)."""
    resp = youtube.captions().list(part="snippet", videoId=video_id).execute()
    return bool(resp.get("items"))


def insert_caption(youtube, video_id: str, srt: Path, language="en", name="English",
                   waits=None):
    """Upload an .srt as a caption track (captions.insert; needs youtube.force-ssl).

    Pass waits=FRESH_CAPTION_WAITS for a video uploaded this run (YouTube 403s
    captions.insert until processing settles); already-live videos get one shot.
    Best-effort at the call site — a failure never blocks upload/playlist."""
    from googleapiclient.http import MediaFileUpload
    body = {"snippet": {"videoId": video_id, "language": language,
                        "name": name, "isDraft": False}}
    waits = waits or []
    last = None
    for attempt in range(len(waits) + 1):
        try:
            media = MediaFileUpload(str(srt), mimetype="application/octet-stream",
                                    resumable=False)
            youtube.captions().insert(part="snippet", body=body,
                                      media_body=media).execute()
            return
        except Exception as e:
            last = e
            if attempt >= len(waits):
                break
            print(f"      · captions attempt {attempt + 1} failed "
                  f"(video likely still processing) — retrying in {waits[attempt]}s")
            time.sleep(waits[attempt])
    raise last


def upload_video(youtube, folder: Path, privacy: str, kind: str = "long", add_anchor: bool = True,
                 ledger: dict | None = None, staged_entry: dict | None = None,
                 topost_mp4: Path | None = None):
    from googleapiclient.http import MediaFileUpload
    sheet = json.loads((folder / "beat_sheet.json").read_text())
    md = sheet["metadata"]
    slug = md["slug"]

    # ── source file: TOPOST master when staged, reel mp4/ otherwise ──────────
    mp4 = topost_mp4 if topost_mp4 is not None else folder / "mp4" / f"{slug}.mp4"
    if not mp4.exists():
        raise SystemExit(f"[yt] no master mp4: {mp4}"
                         + (" — run the 'post' skill to stage a hi-res master" if topost_mp4 else
                            " — run sandwich.py first"))

    # ── metadata: staged.json entry + TOPOST/<slug>.md, or reel fallbacks ────
    if staged_entry is not None:
        title_str = staged_entry.get("title") or md.get("title", "")
        tags_list = staged_entry.get("tags") or md.get("tags") or []
        desc_md   = TOPOST / f"{slug}.md"
        description = (desc_md.read_text() if desc_md.exists() else
                       ((folder / "description.txt").read_text()
                        if (folder / "description.txt").exists() else title_str))
    else:
        title_str   = md.get("title", "")
        tags_list   = md.get("tags") or []
        desc        = folder / "description.txt"
        description = desc.read_text() if desc.exists() else title_str

    if not tags_list:
        tags_list = ["Quantum Mechanics", "Physics", "NotebookLM", "Medhavy",
                     md.get("chapter_title", "")]

    if add_anchor:
        # a derived short funnels to its parent long (looked up in the ledger)
        parent_url, parent_title = "", ""
        if kind == "short":
            parent = md.get("derived_from", "")
            pvid = (ledger or {}).get(parent)
            if pvid:
                parent_url = f"https://youtu.be/{pvid}"
                parent_title = md.get("title", "")
        link = parent_url or (ANCHOR_VIDEO_URL if kind == "short" else ANCHOR_PLAYLIST_URL)
        if link and link not in description:            # idempotent: don't double-append
            description = description.rstrip() + anchor_block(kind, parent_url, parent_title)

    body = {
        "snippet": {
            "title": title_str[:100],
            "description": description,
            "categoryId": EDU_CATEGORY,
            "tags": tags_list[:15],
        },
        "status": {"privacyStatus": "public" if privacy == "public" else "unlisted",
                   "selfDeclaredMadeForKids": False},
    }
    media = MediaFileUpload(str(mp4), chunksize=-1, resumable=True, mimetype="video/mp4")
    req = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
    print(f"[yt] uploading {mp4.name} …")
    resp = None
    while resp is None:
        status, resp = req.next_chunk()
        if status:
            print(f"    {int(status.progress()*100)}%")
    vid = resp["id"]
    print(f"[yt] uploaded → https://youtu.be/{vid}")
    return vid


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("folders", nargs="*", help="explicit video folders")
    ap.add_argument("--root", help="scan this dir for video folders (each has beat_sheet.json)")
    ap.add_argument("--playlist", default=os.getenv("ART_PLAYLIST", ""),
                    help="playlist title to find-or-create (default: $ART_PLAYLIST env var; required)")
    ap.add_argument("--privacy", choices=["unlisted", "public"], default="unlisted")
    ap.add_argument("--channel", default=os.getenv("ART_YOUTUBE_CHANNEL", "nikbearbrown"),
                    help="channel key → youtube/credentials/<channel>/ (default: $ART_YOUTUBE_CHANNEL or nikbearbrown)")
    ap.add_argument("--client", default=None)
    ap.add_argument("--token", default=None)
    ap.add_argument("--ledger", default=None)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--kind", choices=["long", "short"], default="long",
                    help="long → description points to the series PLAYLIST; short → to the intro VIDEO "
                         "(auto-detected for short/ subfolders regardless)")
    ap.add_argument("--no-anchor", action="store_true",
                    help="do not append the default series cross-link to the description")
    ap.add_argument("--no-captions", action="store_true",
                    help="do NOT upload the <slug>.srt caption track with each video")
    args = ap.parse_args()

    folders = [Path(f).expanduser().resolve() for f in args.folders]
    if args.root:
        root = Path(args.root).expanduser().resolve()
        folders += [p.parent for p in root.glob("*/beat_sheet.json")]
    folders = sorted(set(folders),
                     key=lambda f: json.loads((f / "beat_sheet.json").read_text())
                     ["metadata"].get("chapter_number") or 999)
    if not folders:
        sys.exit("[yt] no video folders found (need --root or explicit folders)")
    if not args.playlist:
        # SHORTS ALWAYS POST TO "Shorts": when every folder in the run is a
        # short and no playlist was named, that rule fills it in.
        if all(folder_kind(f, args.kind) == "short" for f in folders):
            args.playlist = "Shorts"
            print('[yt] all folders are shorts → playlist "Shorts" (the standing rule)')
        else:
            sys.exit("[yt] --playlist is required (or set $ART_PLAYLIST in .env)")

    print("[yt] publish order (by chapter):")
    for f in folders:
        m = json.loads((f / "beat_sheet.json").read_text())["metadata"]
        print(f"   ch{m.get('chapter_number')}  {m['title']}")

    if args.dry_run:
        print("[yt] dry-run — authenticating read-only preview")

    _repo = Path(os.environ.get("ART_HOME") or Path(__file__).resolve().parents[4])  # repo root
    _cred = _repo / "youtube" / "credentials" / args.channel
    client_p = Path(args.client).resolve() if args.client else _cred / "client_secret.json"
    token_p  = Path(args.token).resolve()  if args.token  else _cred / "youtube_token.json"
    if not client_p.exists():
        sys.exit(f"[yt] no client_secret at {client_p} — put OAuth creds in "
                 f"youtube/credentials/{args.channel}/ (see .env.example)")
    youtube = get_service(client_p, token_p)
    _expected = ""
    _eid_file = _cred / "expected_channel_id.txt"
    if _eid_file.exists():
        _expected = _eid_file.read_text().strip()
    verify_authenticated_channel(youtube, expected_id=_expected)
    playlist_id = find_or_create_playlist(youtube, args.playlist, args.privacy, args.dry_run)
    in_pl = already_in_playlist(youtube, playlist_id) if (playlist_id and not args.dry_run) else {}

    ledger_path = (Path(args.ledger).resolve() if args.ledger else _cred / "youtube_publish_ledger.json")
    if ledger_path.exists():
        _raw = json.loads(ledger_path.read_text())
        # Normalize: list format [{videoId, file, ...} | "videoId"] → dict keyed by slug/stem
        if isinstance(_raw, list):
            ledger: dict = {}
            for _e in _raw:
                if isinstance(_e, dict):
                    _stem = Path(_e.get("file", "")).stem
                    if _stem:
                        ledger[_stem] = _e.get("videoId", "")
                # plain-string entries (bare video IDs with no slug) are skipped — no key to map
        else:
            ledger = _raw
    else:
        ledger = {}

    for pos, folder in enumerate(folders):
        slug = json.loads((folder / "beat_sheet.json").read_text())["metadata"]["slug"]
        fresh = False
        if slug in ledger:
            vid = ledger[slug]
            print(f"[yt] {slug} already uploaded → {vid}")
        elif args.dry_run:
            print(f"[yt] (dry-run) would upload {slug}")
            if not args.no_captions and (folder / f"{slug}.srt").exists():
                print(f"[yt] (dry-run) would upload caption track {slug}.srt")
            continue
        else:
            kind = folder_kind(folder, args.kind)
            # ── TOPOST preflight — locate the staged master, then gate-check ───
            if not STAGED_JSON.exists():
                sys.exit(f"[yt] ABORT — staged.json not found at {STAGED_JSON}\n"
                         f"    Run the 'post' skill to stage a hi-res master before publishing.")
            staged_all = json.loads(STAGED_JSON.read_text())
            # Resolve the mp4 filename from either format
            _entry_pre = _staged_find(staged_all, f"{slug}.mp4", slug)
            if _entry_pre is None:
                sys.exit(f"[yt] ABORT — '{slug}' has no entry in staged.json\n"
                         f"    staged.json: {STAGED_JSON}\n"
                         f"    Run the 'post' skill to stage this video before publishing.")
            # Derive the filename: new format has files.master_4k; old format keyed by filename
            _master_4k = (_entry_pre.get("files") or {}).get("master_4k") or f"{slug}.mp4"
            topost_mp4 = TOPOST / _master_4k
            staged_entry = topost_preflight(topost_mp4)
            _pre_upload_assert(topost_mp4, staged_entry, ledger)
            vid = upload_video(youtube, folder, args.privacy, kind=kind,
                               add_anchor=not args.no_anchor, ledger=ledger,
                               staged_entry=staged_entry, topost_mp4=topost_mp4)
            update_staged_status(topost_mp4, vid)
            ledger[slug] = vid
            # Record sha256 in the ledger (duplicate-upload guard for re-runs)
            _file_sha = _sha256_file(topost_mp4) if topost_mp4.exists() else ""
            if _file_sha:
                ledger.setdefault("_uploaded_sha256s", [])
                if _file_sha not in ledger["_uploaded_sha256s"]:
                    ledger["_uploaded_sha256s"].append(_file_sha)
            ledger_path.write_text(json.dumps(ledger, indent=1))
            fresh = True

        if playlist_id and not args.dry_run and vid not in in_pl:
            try:
                youtube.playlistItems().insert(
                    part="snippet",
                    body={"snippet": {"playlistId": playlist_id,
                                      "position": pos,
                                      "resourceId": {"kind": "youtube#video", "videoId": vid}}},
                ).execute()
                print(f"[yt] added {slug} to playlist at position {pos}")
                time.sleep(1)
            except Exception as _pl_err:
                print(f"[yt] WARNING: playlist insertion failed (video unaffected): {_pl_err}")
                print(f"[yt] Fix: set playlist '{args.playlist}' to Manual ordering in YouTube Studio, then re-run.")

        # ── captions (CC data) — best-effort, idempotent, never blocks ──────
        if not args.dry_run and not args.no_captions:
            srt = folder / f"{slug}.srt"
            if not srt.exists():
                print(f"[yt] {slug}: no {slug}.srt — skipping captions")
            else:
                try:
                    if has_caption_track(youtube, vid):
                        print(f"[yt] {slug}: caption track already present — skipping")
                    else:
                        print(f"[yt] uploading captions {srt.name} …")
                        insert_caption(youtube, vid, srt,
                                       waits=FRESH_CAPTION_WAITS if fresh else None)
                        print(f"[yt] {slug}: caption track added")
                except Exception as e:
                    print(f"[yt] WARNING: captions for {slug} failed "
                          f"(video unaffected): {e}")

    print("[yt] done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
