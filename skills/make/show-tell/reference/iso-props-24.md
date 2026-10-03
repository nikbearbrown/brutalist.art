# Isometric prop pack: 24 teaching objects

**Legacy, not recommended for new work.** Bear rejected the adapted library
and approved the [25 original props](original-props-25.md) on 2026-10-01.
This reference and its assets remain for reproducing older films. Existing
uses still require the attribution below.

Read this when a beat needs context, tools, human judgment, permissions,
evidence, or workflow props. The pack adds choices; it does not require a
quota or replace the original box/page/server kit.

- Inspect `../assets/isocons-24/adapted-contact.png` and `manifest.json`.
- Paste `templates/iso_kit.py`, then `templates/iso_props_24.py`, into the
  reel's `scenes.py`. Gate A receives that file alone; do not import a sibling.
- `make_prop('shield-lock', x=-1, y=0, scale=1.8)` returns a VGroup.
  `prop.parts['shackle']` is independently movable. Manifest lists every part.
- Editable standalone SVGs with named `<g id>` layers are in
  `assets/isocons-24/svg/`. All have transparent backgrounds and vector paths.
- Select props whose action explains the narration. A shield is not evidence
  that software is safe; a check is not an empirical evaluation; a receipt
  represents a record, not proof that its contents are true.
- Keep one large illustration per beat, at most three short labels, and use
  the same objects for recurring concepts. The showcase demonstrates the whole
  pack because the pack is its subject; normal films should choose a small cast.
- Preserve attribution from `../assets/isocons-24/ATTRIBUTION.md` in copied
  packs and film descriptions. These are simplified redraws, not unchanged
  source SVGs. The original references are for provenance, not film plates.

Regenerate SVGs and previews with `scripts/build_prop_assets.py`. Reference
refresh is explicit (`scripts/fetch_isocons_refs.py`); normal films use the
local assets without contacting the source site.

The worked film lives at `brutalist.art/youtube/show-tell-24-isometric-props/`.
