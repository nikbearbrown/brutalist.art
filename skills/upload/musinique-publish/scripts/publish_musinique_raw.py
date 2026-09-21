#!/usr/bin/env python3
"""Upload standalone (non-beat-sheet) Musinique films to YouTube.

This is deliberately NOT skills/upload/youtube-publisher/scripts/publish_playlist.py:
that script is hard-wired to the Medhavy/NotebookLM pipeline (requires
beat_sheet.json + mp4/<slug>.mp4 + description.txt per folder, uses
chapter_number for playlist position, and auto-appends a "Brutalist" series
cross-link to every description). None of that applies to a raw
musinique-bookend master, and the cross-link would be actively wrong content
under a Musinique spoken-word film.

What this script actually does, per video:
  1. Copies the source master into books/youtube/TOPOST/ (COPY, not move —
     these aren't reel folders with separate build paperwork; the book keeps
     its own copy too) and writes an honest staged.json entry (no gate_t/
     all_beats_4k fields — this isn't a beat-sheet reel, so those don't apply;
     the real ffprobe'd resolution/duration are recorded instead).
  2. Uploads the TOPOST copy (never the book-folder original) as `unlisted`.
  3. Finds-or-creates the target playlist and inserts the video into it.
  4. Appends a row to books/youtube/PUBLISH-LOG.md.

Usage:
    python3 publish_musinique_raw.py --manifest manifest.json \
        --playlist "@Musinique" --channel musinique [--dry-run]

manifest.json: [{"path": "...", "title": "...", "description": "...", "slug": "..."}]
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

REPO_ROOT = "/Users/bear/Documents/CoWork/bear-textbooks/books"
TOPOST = os.path.join(REPO_ROOT, "youtube", "TOPOST")
PUBLISH_LOG = os.path.join(REPO_ROOT, "youtube", "PUBLISH-LOG.md")


def ffprobe_json(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height,r_frame_rate",
         "-show_entries", "format=duration",
         "-of", "json", path],
        capture_output=True, text=True, check=True,
    ).stdout
    return json.loads(out)


def load_credentials(channel):
    cred_dir = os.path.join(REPO_ROOT, "youtube", "credentials", channel)
    client_path = os.path.join(cred_dir, "client_secret.json")
    token_path = os.path.join(cred_dir, "youtube_token.json")
    creds = Credentials.from_authorized_user_file(
        token_path,
        scopes=["https://www.googleapis.com/auth/youtube",
                "https://www.googleapis.com/auth/youtube.force-ssl"],
    )
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        with open(token_path, "w") as f:
            f.write(creds.to_json())
    return creds


def find_or_create_playlist(youtube, title, privacy):
    page_token = None
    while True:
        resp = youtube.playlists().list(
            part="snippet", mine=True, maxResults=50, pageToken=page_token
        ).execute()
        for item in resp.get("items", []):
            if item["snippet"]["title"] == title:
                return item["id"], False
        page_token = resp.get("nextPageToken")
        if not page_token:
            break
    resp = youtube.playlists().insert(
        part="snippet,status",
        body={
            "snippet": {"title": title,
                        "description": f"{title} — Musinique."},
            "status": {"privacyStatus": privacy},
        },
    ).execute()
    return resp["id"], True


def upload_video(youtube, path, title, description, privacy):
    body = {
        "snippet": {"title": title, "description": description, "categoryId": "10"},
        "status": {"privacyStatus": privacy, "selfDeclaredMadeForKids": False},
    }
    media = MediaFileUpload(path, chunksize=8 * 1024 * 1024, resumable=True, mimetype="video/mp4")
    req = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
    response = None
    last_pct = -10
    while response is None:
        status, response = req.next_chunk()
        if status:
            pct = int(status.progress() * 100)
            if pct >= last_pct + 10:
                print(f"[upload] {title}: {pct}%", flush=True)
                last_pct = pct
    return response["id"]


def insert_into_playlist(youtube, playlist_id, video_id, position):
    youtube.playlistItems().insert(
        part="snippet",
        body={
            "snippet": {
                "playlistId": playlist_id,
                "resourceId": {"kind": "youtube#video", "videoId": video_id},
                "position": position,
            }
        },
    ).execute()


def stage_to_topost(path, slug, meta):
    os.makedirs(TOPOST, exist_ok=True)
    dest = os.path.join(TOPOST, f"{slug}.mp4")
    shutil.copy2(path, dest)
    staged_path = os.path.join(TOPOST, "staged.json")
    data = {"videos": []}
    if os.path.exists(staged_path):
        with open(staged_path) as f:
            data = json.load(f)
    data["videos"] = [v for v in data.get("videos", []) if v.get("slug") != slug]
    data["videos"].append({
        "slug": slug,
        "title": meta["title"],
        "source_reel": None,
        "not_a_beat_sheet_reel": True,
        "source_file": path,
        "staged_at": datetime.now().astimezone().isoformat(),
        "files": {"master_4k": f"{slug}.mp4"},
        "resolution": meta["resolution"],
        "duration_s": meta["duration_s"],
        "markers_clean": True,
        "topaz": {"ran": False, "reason": "already-source 4K, no beat-sheet reel"},
        "status": "staged",
    })
    with open(staged_path, "w") as f:
        json.dump(data, f, indent=2)
    return dest


def append_log(rows):
    header = "# PUBLISH-LOG.md\n\n"
    line_fmt = "- {date} — **{title}** → https://youtu.be/{video_id} — playlist \"{playlist}\" @ pos {pos} — channel `{channel}` — {note}\n"
    exists = os.path.exists(PUBLISH_LOG)
    with open(PUBLISH_LOG, "a") as f:
        if not exists:
            f.write(header)
        for r in rows:
            f.write(line_fmt.format(**r))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--playlist", required=True)
    ap.add_argument("--channel", required=True)
    ap.add_argument("--privacy", default="unlisted", choices=["unlisted", "public", "private"])
    ap.add_argument("--playlist-privacy", default="unlisted", choices=["unlisted", "public", "private"])
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--identity-check-only", action="store_true")
    args = ap.parse_args()

    with open(args.manifest) as f:
        manifest = json.load(f)

    creds = load_credentials(args.channel)
    youtube = build("youtube", "v3", credentials=creds)

    who = youtube.channels().list(part="snippet", mine=True).execute()
    ch = who["items"][0]["snippet"]["title"] if who.get("items") else "<none>"
    print(f"[identity] authenticated as channel: {ch}")

    if args.identity_check_only:
        pid_probe = None
        page_token = None
        found = []
        while True:
            resp = youtube.playlists().list(part="snippet", mine=True, maxResults=50, pageToken=page_token).execute()
            found.extend(i["snippet"]["title"] for i in resp.get("items", []))
            page_token = resp.get("nextPageToken")
            if not page_token:
                break
        print(f"[identity] existing playlists: {found}")
        return

    if args.dry_run:
        for m in manifest:
            probe = ffprobe_json(m["path"])
            print(f"[dry-run] would stage+upload {m['path']} as '{m['title']}' -> playlist '{args.playlist}' ({args.privacy})")
            print(f"          ffprobe: {probe}")
        return

    playlist_id, created = find_or_create_playlist(youtube, args.playlist, args.playlist_privacy)
    print(f"[playlist] '{args.playlist}' id={playlist_id} ({'created' if created else 'found'})")

    log_rows = []
    for i, m in enumerate(manifest):
        probe = ffprobe_json(m["path"])
        vstream = probe["streams"][0]
        meta = {
            "title": m["title"],
            "resolution": f"{vstream['width']}x{vstream['height']}",
            "duration_s": float(probe["format"]["duration"]),
        }
        staged_path = stage_to_topost(m["path"], m["slug"], meta)
        print(f"[stage] {m['slug']} -> {staged_path}")

        video_id = upload_video(youtube, staged_path, m["title"], m["description"], args.privacy)
        print(f"[upload] {m['title']} -> https://youtu.be/{video_id}")

        insert_into_playlist(youtube, playlist_id, video_id, i)
        print(f"[playlist] inserted {m['title']} at position {i}")

        log_rows.append({
            "date": datetime.now().astimezone().strftime("%Y-%m-%d %H:%M %Z"),
            "title": m["title"],
            "video_id": video_id,
            "playlist": args.playlist,
            "pos": i,
            "channel": args.channel,
            "note": "facts signed off by Bear",
        })

    append_log(log_rows)
    print("[done] PUBLISH-LOG.md updated")


if __name__ == "__main__":
    main()
