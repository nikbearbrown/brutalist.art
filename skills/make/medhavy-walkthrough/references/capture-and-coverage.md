# Capture and coverage (web)

## Tenant choice comes first

| Tenant | Allowed? | Notes |
|---|---|---|
| Seeded local (`npm run dev`, dev Supabase, fictional users) | **Default** | Seed via the Feature-Testing-Manual phases; name users obviously fake. |
| Staging with fictional data | Yes | Record the base URL and who confirmed the data is fictional. |
| Production `hub.medhavy.com` | Only with redaction | Every frame with a name, email, `CLS-` code, analytics row, or PostHog id is redacted before hashing. `privacy.data_source = "redacted-live"` and a `redaction_log` are mandatory. |

Redaction happens on the raw capture **before** the evidence hash is taken,
because the hash is what the validator trusts. Re-hashing after a late blur
is fine; forgetting one frame is not. Blur boxes are logged as
`{capture, start_s, end_s, box:[x0,y0,x1,y1], what}` in `capture/redaction.jsonl`.

## Sign-in is the human's

The agent never types a password, one-time code, or key, and never creates an
account. The human signs in to Clerk in the capture browser. Two routes:

- **Playwright, scripted.** Human signs in once via
  `scripts/save_session.py` (headed Chromium; saves `storageState` to
  `~/.medhavy-walkthrough/`, **outside the reel**) (it is a session credential,
  never evidence). The driver launches with that state, viewport
  `3840×2160`, `deviceScaleFactor: 1`, `recordVideo` at the same size, and logs
  every action as `{t_ms, action, selector_or_text, url_after}` to
  `capture/run-01-actions.jsonl`. Assert the expected DOM outcome after each
  step and exit nonzero on failure; running out of steps is not success.
- **Human-driven.** The human clicks; a screen recorder captures the native
  4K window; the human keeps timecoded notes in the same JSONL shape.

Playwright's own recorder writes WebM; transcode losslessly to MP4 for
`capture/`, then hash the MP4. Keep the WebM until the film is verified.
Do not capture at 1080p and upscale; a display-clamped window is a blocker to
report, not to hide. Check the first 10 s of one pilot take before a full run.

Cross-role flows use two browser contexts (student, admin) in one driver run,
or two runs. Either way, the beat sheet says which context is on screen; an
edit that hides a role switch reads as a lie.

The textbook-open handoff leaves the hub. If a registered textbook site is
reachable, follow the token into it and show the protected page load; if not,
stop at the hub's redirect and say so in `CAPTURE.md` and the Verdict.

## Timing and audio contract

Keep the real click → response interval at normal speed. Next.js route
transitions and Supabase round-trips are part of the evidence; if a page is
slow, the riff can say so. Split narration or add a **labeled** hold outside
the interval; never speed up or slow down the capture to fit a sentence.
Do not run `pantry` on captures. Pre-trim each `media/Bxx.mp4` and match
`render_duration_s` to the clip at the film frame rate.

The hub has no meaningful audio. Liam is the only voice; no click sounds,
notification chimes, or synthesized UI audio. The outro card carries only
Liam re-reading the title and "At Nik Bear Brown"; no jingle, no music.

## `coverage.json` contract

```json
{
  "schema_version": 1,
  "site": {
    "name": "medhavy-hub",
    "build_id": "<source-snapshot-sha256>",
    "base_url": "http://localhost:3000"
  },
  "privacy": {
    "data_source": "seeded-demo",
    "redaction_log": null
  },
  "captures": {
    "run-01": {
      "path": "capture/run-01.mp4",
      "sha256": "<capture-file-sha256>",
      "build_id": "<same-source-snapshot-sha256>",
      "method": "scripted-browser",
      "context": "student",
      "action_log": "capture/run-01-actions.jsonl"
    }
  },
  "features": [
    {
      "id": "student-request-access", "role": "student", "status": "implemented",
      "evidence": [{
        "capture": "run-01", "beat_id": "B04",
        "start_s": 12.0, "action_s": 13.4, "end_s": 16.0,
        "observation": "Request button on a private textbook card turns to Pending.",
        "riff": "Write after inspecting this take."
      }]
    },
    {"id": "memory-api", "role": "service", "status": "api-only",
     "reason": "Service-to-service; no screen.", "transcript": "capture/memory-api.txt",
     "evidence": []},
    {"id": "password-change-invalidation", "role": "admin", "status": "planned",
     "reason": "Wired but dormant per DEVELOPER.md §4.5.", "evidence": []}
  ]
}
```

- `data_source` is `seeded-demo`, `staging-fictional`, or `redacted-live`;
  the last requires a nonempty `redaction_log` path inside the reel.
- `method` is `scripted-browser` or `human-browser`; both need an action log.
- `status` is `implemented` (needs evidence), `planned` (needs reason, no
  evidence), or `api-only` (needs reason and a transcript file; no evidence).
  Do not relabel a broken UI feature as `api-only` or `planned` to pass.
- Every `role` is `student`, `instructor`, `admin`, `service`, or `public`.
- `beat_id`s must exist in `beat_sheet.json` with narration.

The sample values are not evidence. Run `./art medhavy-walkthrough --check REEL`
before assembly and after every change. `--min-height 720` exists for a pilot
only. The machine check cannot see whether a blur covers the whole email or
whether the source inventory missed a tab; those go in `_qc/REPORT.md`.
