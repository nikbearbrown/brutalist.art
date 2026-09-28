"""
iso_kit.py — the show-tell drawing kit. PASTE this block at the top of a reel's scenes.py;
do not import it (Gate A copies only scenes.py into its sandbox).

Drawn isometric objects in the Claude palette: cardboard boxes (closed, open, taped), dark
MCP blocks with ports, flat skill pages, server stacks with lights, checks, a cursor, pills.
Pacing helpers read the reel's beat_sheet.json so scenes wait for their spoken phrase.

Every rule in ../SKILL.md "DRAWING LAWS" is already obeyed by these primitives; keep it that
way when you add one (label beside, never inside; terracotta never under text; dim greys
with gaps for chart blocks; type floor 32).
"""
from manim import *
import numpy as np
import json as _json, os as _os

# ═════════════════════════════ ISO KIT (show-tell) ═════════════════════════════
STAGE = "#F2F0E9"; INK = "#3D3929"; TERRA = "#D97757"; DIM = "#8B8F96"; GHOST = "#D9D4C7"; CARD = "#FAF9F5"
BOX_TOP, BOX_L, BOX_R = "#F3E9D8", "#DCC9AA", "#C7AE86"          # kraft cardboard: top, left face, right face (deep enough for Gate V contrast)
BOX_IN1, BOX_IN2, BOX_FLOOR = "#CDB894", "#BFA67E", "#B39A72"     # inside walls + floor
DARK_TOP, DARK_L, DARK_R = "#3A3530", "#26221F", "#1E1B18"        # MCP / server blocks
PAGE_TOP, PAGE_L, PAGE_R = "#FFFFFF", "#ECE7DF", "#E2DCD2"         # skill pages
BAR1, BAR2, BAR3 = "#8B8F96", "#B4AFA6", "#D9D4C7"                # chart segments, dim to ghost
SERIF = "EB Garamond"
C30 = 0.8660254
config.background_color = STAGE


def T(s, size=36, color=INK, bold=False):
    return Text(s, font=SERIF, color=color, font_size=size, weight="BOLD" if bold else "NORMAL")


class Iso:
    """Isometric projection: x runs right-up, y runs left-up, z runs up. (ox, oy) is where (0,0,0) lands."""
    def __init__(self, ox=0.0, oy=0.0, s=1.0):
        self.ox, self.oy, self.s = ox, oy, s

    def p(self, x, y, z=0.0):
        return np.array([self.ox + (x - y) * C30 * self.s, self.oy + (x + y) * 0.5 * self.s + z * self.s, 0.0])

    def v(self, dx, dy, dz=0.0):
        return self.p(dx, dy, dz) - self.p(0, 0, 0)

    def quad(self, pts, fill, stroke=INK, sw=4):
        return Polygon(*[self.p(*q) for q in pts], fill_color=fill, fill_opacity=1, stroke_color=stroke, stroke_width=sw)

    def box(self, x0, y0, z0, w, d, h, top=BOX_TOP, left=BOX_L, right=BOX_R, sw=4):
        """Closed box: the two front faces (x = x0 and y = y0) plus the top."""
        x1, y1, z1 = x0 + w, y0 + d, z0 + h
        return VGroup(
            self.quad([(x0, y0, z0), (x0, y1, z0), (x0, y1, z1), (x0, y0, z1)], left, sw=sw),
            self.quad([(x0, y0, z0), (x1, y0, z0), (x1, y0, z1), (x0, y0, z1)], right, sw=sw),
            self.quad([(x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)], top, sw=sw))

    def open_box(self, x0, y0, z0, w, d, h):
        """(back, front): floor + inner back walls, then the front walls. Put contents between them."""
        x1, y1, z1 = x0 + w, y0 + d, z0 + h
        back = VGroup(
            self.quad([(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0)], BOX_FLOOR),
            self.quad([(x1, y0, z0), (x1, y1, z0), (x1, y1, z1), (x1, y0, z1)], BOX_IN1),
            self.quad([(x0, y1, z0), (x1, y1, z0), (x1, y1, z1), (x0, y1, z1)], BOX_IN2))
        front = VGroup(
            self.quad([(x0, y0, z0), (x0, y1, z0), (x0, y1, z1), (x0, y0, z1)], BOX_L),
            self.quad([(x0, y0, z0), (x1, y0, z0), (x1, y0, z1), (x0, y0, z1)], BOX_R))
        back.set_z_index(0); front.set_z_index(2)
        return back, front

    def tape(self, x0, y0, z1, w, d, drop=0.35, t=0.22):
        """Terracotta tape across the top (along x) and down the left front face."""
        ym = y0 + d / 2
        return VGroup(
            self.quad([(x0, ym - t, z1), (x0 + w, ym - t, z1), (x0 + w, ym + t, z1), (x0, ym + t, z1)], TERRA, sw=0),
            self.quad([(x0, ym - t, z1), (x0, ym + t, z1), (x0, ym + t, z1 - drop), (x0, ym - t, z1 - drop)], TERRA, sw=0))

    def mcp(self, x0, y0, z0, w=1.3, d=1.3, h=0.7):
        """Dark MCP block with two light ports on its right front face."""
        body = self.box(x0, y0, z0, w, d, h, DARK_TOP, DARK_L, DARK_R)
        ports = VGroup(*[self.box(x0 + w * f, y0 - 0.18, z0 + h * 0.3, w * 0.16, 0.18, h * 0.3, GHOST, BOX_IN1, BOX_IN2, sw=1)
                         for f in (0.22, 0.58)])
        return VGroup(body, ports)

    def page(self, x0, y0, z0, w=1.1, d=1.4):
        """A skill page lying flat: white slab, three ghost text lines, one terracotta dot."""
        slab = self.box(x0, y0, z0, w, d, 0.06, PAGE_TOP, PAGE_L, PAGE_R, sw=1.5)
        zt = z0 + 0.06
        lines = VGroup(*[Line(self.p(x0 + 0.2, y0 + d * f, zt), self.p(x0 + w - 0.2, y0 + d * f, zt), color=GHOST, stroke_width=4)
                         for f in (0.3, 0.5, 0.7)])
        dot = Dot(self.p(x0 + 0.2, y0 + d * 0.86, zt), radius=0.06, color=TERRA)
        return VGroup(slab, lines, dot)

    def server(self, x0, y0, z0, w=1.4, d=1.4, slab=0.42, n=3):
        """A stack of dark server slabs; returns (stack, lights) — lights start ghost, turn terracotta."""
        stack = VGroup(*[self.box(x0, y0, z0 + i * (slab + 0.04), w, d, slab, DARK_TOP, DARK_L, DARK_R) for i in range(n)])
        lights = VGroup(*[Dot(self.p(x0 + 0.25, y0, z0 + i * (slab + 0.04) + slab / 2), radius=0.06, color=GHOST) for i in range(n)])
        return stack, lights


def ease_in(t):
    """Quadratic ease-in (things dropping into a box). Local: Gate A's stub has no ease_in_quad."""
    return t * t


def check(x, y, s=0.2, color=INK, w=7):
    return VGroup(Line([x - s, y, 0], [x - s * 0.3, y - s * 0.75, 0], color=color, stroke_width=w),
                  Line([x - s * 0.3, y - s * 0.75, 0], [x + s * 1.1, y + s * 0.85, 0], color=color, stroke_width=w))


def cursor(x, y, s=0.45):
    return Polygon([x, y, 0], [x, y - s, 0], [x + s * 0.28, y - s * 0.72, 0], [x + s * 0.62, y - s * 0.66, 0],
                   fill_color=INK, fill_opacity=1, stroke_color=CARD, stroke_width=2)


def pill(x, y, w, h=0.62, fill="#FFFFFF"):
    return RoundedRectangle(width=w, height=h, corner_radius=h / 2, fill_color=fill, fill_opacity=1, stroke_width=0).move_to([x, y, 0])


# ═════════════════════════════ pacing (narration is the clock) ═════════════════════════════
try:
    _SHEET = _json.load(open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "beat_sheet.json")))
    _TARGET = {b["beat_id"]: float(b.get("actual_duration_s") or b.get("estimated_duration_s") or 0) for b in _SHEET["beats"]}
    _NARR = {b["beat_id"]: b["narration_text"] for b in _SHEET["beats"]}
except Exception:
    _TARGET, _NARR = {}, {}


def _elapsed(self):
    rt = getattr(getattr(self, "renderer", None), "time", None)
    return float(rt) if isinstance(rt, (int, float)) else 0.0


def until(self, phrase, lead=0.25):
    """Wait until `phrase` is spoken (its character share of the narration × the measured audio)."""
    bid = type(self).__name__.split("_")[0]
    n, target = _NARR.get(bid, ""), _TARGET.get(bid, 0)
    if not n or not target or phrase not in n:
        return
    gap = target * n.index(phrase) / len(n) - lead - _elapsed(self)
    if gap > 0.05:
        self.wait(gap)


def finish(self):
    target = _TARGET.get(type(self).__name__.split("_")[0], 0)
    self.wait(max(0.3, target - _elapsed(self)) if target else 2.0)


# ═════════════════════════════ the film ═════════════════════════════
# claude-liam-brutalist-show-tell-cards — the three DRAWN beats (B00, B01, B10). The eight card
# beats are ShowTellCard compositions (Remotion), rendered by remotion_scenes.py.
BOXW, BOXD, BOXH, LIDH = 3.0, 3.0, 1.9, 0.22
MAIN = Iso(0.0, -2.0, 0.78)          # the hero box, centre stage
LEFT_BOX = Iso(-3.2, -1.9, 0.7)      # B00: the box shares the stage with the voice


def floor_shadow(iso=MAIN):
    sh = iso.quad([(0.15, -0.35, 0), (BOXW + 0.35, -0.35, 0), (BOXW + 0.35, BOXD - 0.15, 0), (0.15, BOXD - 0.15, 0)], "#BFB4A0", sw=0)
    sh.set_z_index(-1)
    return sh


def sealed(iso=MAIN):
    return VGroup(iso.box(0, 0, 0, BOXW, BOXD, BOXH), iso.tape(0, 0, BOXH, BOXW, BOXD))


VOICE_H = [0.6, 1.3, 2.1, 1.1, 2.6, 1.6, 0.9, 1.9, 0.7]


def voice_bars(heights, x0=1.5, gap=0.4, w=0.24, y=0.0):
    return VGroup(*[RoundedRectangle(width=w, height=h, corner_radius=w / 2, fill_color=DIM, fill_opacity=1, stroke_width=0)
                    .move_to([x0 + i * gap, y, 0]) for i, h in enumerate(heights)])


class B00_ShowTell(Scene):
    def construct(self):
        box = sealed(LEFT_BOX)
        box.shift(UP * 3.4)
        self.add(box)
        self.play(box.animate.shift(DOWN * 3.4), run_time=1.1, rate_func=rate_functions.ease_out_bounce)
        self.play(FadeIn(floor_shadow(LEFT_BOX)), run_time=0.4)
        until(self, "and the voice")
        bars = voice_bars(VOICE_H)
        self.play(LaggedStart(*[GrowFromCenter(b) for b in bars], lag_ratio=0.12), run_time=1.2)
        until(self, "The picture shows")
        self.play(FadeIn(T("show", 44).move_to([-3.2, -2.75, 0]), shift=UP * 0.2), run_time=0.6)
        until(self, "The voice tells")
        self.play(FadeIn(T("tell", 44).move_to([3.1, -2.75, 0]), shift=UP * 0.2),
                  *[b.animate.stretch_to_fit_height(VOICE_H[(i + 3) % len(VOICE_H)]) for i, b in enumerate(bars)], run_time=0.8)
        finish(self)


class B01_Kit(Scene):
    def construct(self):
        box = sealed()
        self.add(floor_shadow(), box)
        back, front = MAIN.open_box(0, 0, 0, BOXW, BOXD, BOXH)
        lid = VGroup(MAIN.box(0, 0, BOXH, BOXW, BOXD, LIDH), MAIN.tape(0, 0, BOXH + LIDH, BOXW, BOXD, drop=LIDH))
        lid.set_z_index(3)
        until(self, "one kit")
        blocks = VGroup(MAIN.mcp(0.4, 0.9, 0.3), MAIN.mcp(1.4, 1.6, 0.3)); blocks.set_z_index(1)
        self.play(FadeOut(box), FadeIn(back), FadeIn(front), FadeIn(lid), FadeIn(blocks), run_time=0.3)
        self.play(lid.animate.shift(UP * 2.4 + RIGHT * 0.6).scale(0.8), run_time=0.7)
        self.play(lid.animate.shift(UP * 2.0).set_opacity(0), run_time=0.4)
        until(self, "dark blocks", lead=0.6)
        self.play(*[b.animate.move_to(t) for b, t in zip(blocks, [np.array([-4.6, 0.9, 0]), np.array([-3.4, -1.0, 0])])], run_time=0.9)
        self.play(FadeIn(T("blocks", 40).move_to([-4.0, -2.35, 0])), run_time=0.4)
        until(self, "flat pages")
        pages = VGroup(MAIN.page(0.8, 0.8, 0.4), MAIN.page(1.6, 1.3, 0.5)); pages.set_z_index(1)
        self.add(pages)
        self.play(*[p.animate.move_to(t) for p, t in zip(pages, [np.array([4.2, 1.1, 0]), np.array([3.5, -0.8, 0])])], run_time=0.9)
        self.play(FadeIn(T("pages", 40).move_to([3.9, -2.35, 0])), run_time=0.4)
        until(self, "Claude's colours")
        self.play(Indicate(blocks, color=None, scale_factor=1.06), Indicate(pages, color=None, scale_factor=1.06), run_time=0.7)
        finish(self)


def paper_card(x, y, w=2.8, h=1.7):
    """A flat ShowTellCard drawn in Manim: kraft offset under a cream card, three dim bars, one terracotta dot."""
    shadow = RoundedRectangle(width=w, height=h, corner_radius=0.16, fill_color=BOX_L, fill_opacity=1, stroke_width=0).move_to([x + 0.1, y - 0.1, 0])
    face = RoundedRectangle(width=w, height=h, corner_radius=0.16, fill_color=CARD, fill_opacity=1, stroke_color=INK, stroke_width=3).move_to([x, y, 0])
    bars = VGroup(*[Rectangle(width=0.34, height=hh, fill_color=BAR2 if i < 2 else BAR1, fill_opacity=1, stroke_width=0)
                    .move_to([x - 0.7 + i * 0.55, y - 0.55 + hh / 2, 0]) for i, hh in enumerate([0.5, 0.8, 1.1])])
    dot = Dot([x + 1.0, y + 0.5, 0], radius=0.11, color=TERRA)
    return VGroup(shadow, face, bars, dot)


class B10_Mix(Scene):
    def construct(self):
        # dim grey: near-black reads as one huge ink "text" blob in GATE T §8.6b; kraft is too pale for Gate V (0.30)
        strip = RoundedRectangle(width=11.4, height=3.2, corner_radius=0.2, fill_color=DIM, fill_opacity=1, stroke_width=0).move_to([0, -0.1, 0])
        frames = VGroup(*[RoundedRectangle(width=4.6, height=2.5, corner_radius=0.12, fill_color=CARD, fill_opacity=1, stroke_width=0)
                          .move_to([x, -0.1, 0]) for x in (-2.7, 2.7)])
        self.play(GrowFromEdge(strip, LEFT), run_time=1.0)
        self.play(LaggedStart(*[GrowFromCenter(f) for f in frames], lag_ratio=0.3), run_time=0.8)
        until(self, "two drawn beats")
        SMALL = Iso(-2.7, -1.05, 0.42)
        box = VGroup(SMALL.box(0, 0, 0, 2.4, 2.4, 1.4), SMALL.tape(0, 0, 1.4, 2.4, 2.4, drop=0.3))
        box.shift(UP * 4.0); self.add(box)
        self.play(box.animate.shift(DOWN * 4.0), run_time=0.9, rate_func=ease_in)
        self.play(FadeIn(T("drawing", 40).move_to([-2.7, -2.4, 0])), run_time=0.4)
        until(self, "Never put two cards")
        cardg = paper_card(2.7, -0.1)
        cardg.shift(UP * 4.0); self.add(cardg)
        self.play(cardg.animate.shift(DOWN * 4.0), run_time=0.9, rate_func=ease_in)
        self.play(FadeIn(T("card", 40).move_to([2.7, -2.4, 0])), run_time=0.4)
        until(self, "its motion is the point")
        badge = Circle(radius=0.42, fill_color=TERRA, fill_opacity=1, stroke_width=0).move_to([0, 2.45, 0])
        tick = check(0.02, 2.47, s=0.2, color=CARD, w=8)
        self.play(GrowFromCenter(badge), run_time=0.4)
        self.play(Create(tick), run_time=0.5)
        finish(self)
