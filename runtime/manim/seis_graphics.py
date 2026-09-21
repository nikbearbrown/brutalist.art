"""seis_graphics.py — the three animated shapes SEIS spotlight reels reuse (brands/seis.md).

Copied into each reel folder by seis_profile.py next to scenes.py; scenes import it locally.
NEU brand law: white ground, black ink, NU red as the ONE emphasis, gray structure, Lato.
Everything here is a PROCESS that moves — a token travels the flow, keys draw between
tables and a query lights a join, rows clean themselves into a table and a chart draws.
Nothing is a slide. Durations come from the beat's measured audio (see beat_dur()).

Shapes:
  FlowStrip(stages)        input → system → output boxes; run_token() animates the path
  SchemaCard / link()      relational tables, FK lines, QueryLine + highlight_join()
  DataPipeline             messy rows → clean table → line chart → named outputs
Pango gotcha: Text() may drop a single space at some word boundaries — keep labels short,
never slant=ITALIC on multi-word text.
"""
import json, os
import numpy as np
from contextlib import contextmanager
from manim import *
try:  # Gate A's static stub has no register_font; the real manim does
    from manim import register_font as _register_font
except Exception:
    try:
        from manim.mobject.text.text_mobject import register_font as _register_font
    except Exception:
        _register_font = None

GROUND = ManimColor("#FFFFFF"); INK = ManimColor("#000000"); RED = ManimColor("#C8102E")
GRAY = ManimColor("#545454"); HAIR = ManimColor("#E3E3E3"); LIGHT = ManimColor("#F4F4F4")
FONT = "Lato"
_HERE = os.path.dirname(os.path.abspath(__file__))
_LATO = [p for p in (
    os.environ.get("LATO_TTF", ""),                                           # explicit override
    os.path.join(_HERE, "fonts", "Lato-Regular.ttf"),                         # copied into the reel by seis_profile.py
    os.path.join(_HERE, "..", "fonts", "Lato", "static", "Lato-Regular.ttf"),  # toolkit copy (runtime/fonts/Lato/static/)
    os.path.join(_HERE, "..", "manim", "fonts", "Lato-Regular.ttf"),          # toolkit copy (runtime/manim/fonts/)
) if p and os.path.exists(p)]


@contextmanager
def lato():
    """Register the bundled Lato for Pango for the duration of construct()."""
    if _LATO and _register_font is not None:
        with _register_font(_LATO[0]):
            yield
    else:
        yield


def beat_dur(bid, default=12.0):
    """The beat's measured narration length — the clock every animation conforms to."""
    try:
        d = json.load(open(os.path.join(_HERE, "beat_sheet.json")))
        for b in d["beats"]:
            if b["beat_id"] == bid:
                return float(b.get("actual_duration_s") or b.get("estimated_duration_s") or default)
    except Exception:
        pass
    return default


def T(s, size=30, color=INK, weight="NORMAL"):
    """Pango may drop a single space at some word boundaries on macOS — write a double space there."""
    return Text(s, font=FONT, font_size=size, color=color, weight=weight)


def rule(scene, width=1.6, at=None):
    """The one red rule every NEU frame carries (brand: every asset contains red)."""
    r = Line(ORIGIN, RIGHT * width, stroke_width=6, color=RED)
    r.move_to(at if at is not None else UP * 3.1 + LEFT * 5.6, aligned_edge=LEFT)
    scene.play(Create(r), run_time=0.5)
    return r


# ── 1. FlowStrip ─────────────────────────────────────────────────────────────
class FlowStrip(VGroup):
    """Boxes left→right with arrows. stages: list of (label, sublabel|None)."""

    def __init__(self, stages, box_w=2.6, box_h=1.3, gap=0.9, size=28, **kw):
        super().__init__(**kw)
        self.boxes, self.arrows = [], []
        for i, (lab, sub) in enumerate(stages):
            box = RoundedRectangle(corner_radius=0.12, width=box_w, height=box_h,
                                   stroke_color=GRAY, stroke_width=2.5, fill_color=GROUND, fill_opacity=1)
            t = T(lab, size).move_to(box)
            g = VGroup(box, t)
            if sub:
                g.add(T(sub, 18, GRAY).next_to(box, DOWN, buff=0.15))
            g.shift(RIGHT * i * (box_w + gap))
            self.boxes.append(g); self.add(g)
        for a, b in zip(self.boxes, self.boxes[1:]):
            ar = Arrow(a[0].get_right(), b[0].get_left(), buff=0.08, stroke_width=3, color=GRAY,
                       max_tip_length_to_length_ratio=0.18)
            self.arrows.append(ar); self.add(ar)
        self.move_to(ORIGIN)

    def draw(self, scene, total=3.0):
        n = len(self.boxes)
        per = total / (2 * n - 1)
        for i, g in enumerate(self.boxes):
            scene.play(FadeIn(g, shift=UP * 0.15), run_time=per)
            if i < n - 1:
                scene.play(Create(self.arrows[i]), run_time=per)

    def run_token(self, scene, total=3.0, hold=0.35):
        """A red dot travels the path; each box it enters gets the red stroke (the ONE emphasis)."""
        # inner bottom edge: under the label, inside the stroke (np.array: Gate A's stub returns lists)
        lane = lambda box: np.array(box.get_bottom()) + UP * 0.14
        entry = lambda box: lane(box) + (np.array(box.get_left()) - np.array(box.get_center())) * np.array([1, 0, 0])
        dot = Dot(radius=0.10, color=RED).move_to(entry(self.boxes[0][0]))
        scene.add(dot)
        legs = len(self.boxes)
        move = (total - hold * legs) / max(1, legs - 1) if legs > 1 else total
        for i, g in enumerate(self.boxes):
            scene.play(dot.animate.move_to(lane(g[0])), run_time=hold * 0.6)
            scene.play(g[0].animate.set_stroke(RED, 4), run_time=hold * 0.4)
            if i < legs - 1:
                scene.play(dot.animate.move_to(entry(self.boxes[i + 1][0])), run_time=move,
                           rate_func=linear)
        scene.play(FadeOut(dot), run_time=0.25)
        return dot


# ── 2. Schema ────────────────────────────────────────────────────────────────
class SchemaCard(VGroup):
    """A relational table: header + field rows. fields: list of str; key fields end with ' *'."""

    def __init__(self, name, fields, w=2.7, size=20, **kw):
        super().__init__(**kw)
        head = Rectangle(width=w, height=0.5, stroke_color=INK, stroke_width=2, fill_color=INK, fill_opacity=1)
        ht = T(name, 22, GROUND).move_to(head)
        body_h = 0.42 * len(fields) + 0.15
        body = Rectangle(width=w, height=body_h, stroke_color=GRAY, stroke_width=2, fill_color=GROUND, fill_opacity=1)
        body.next_to(head, DOWN, buff=0)
        self.rows = {}
        for i, f in enumerate(fields):
            key = f.endswith(" *"); label = f[:-2] if key else f
            r = T(label, size, INK if key else GRAY).move_to(body.get_top() + DOWN * (0.32 + 0.42 * i))
            r.align_to(body.get_left() + RIGHT * 0.2, LEFT)
            self.rows[label] = r
        self.head, self.body = head, body
        self.add(head, ht, body, *self.rows.values())

    def row(self, name):
        return self.rows[name]


def link(a: SchemaCard, fa: str, b: SchemaCard, fb: str):
    """FK line between two rows (gray, draws in)."""
    p1, p2 = a.row(fa), b.row(fb)
    start = p1.get_right() + RIGHT * 0.15 if p1.get_center()[0] < p2.get_center()[0] else p1.get_left() + LEFT * 0.15
    end = p2.get_left() + LEFT * 0.15 if p1.get_center()[0] < p2.get_center()[0] else p2.get_right() + RIGHT * 0.15
    return Line(start, end, stroke_width=2, color=GRAY)


class QueryLine(VGroup):
    """A SQL line in mono, typed in; highlight_join() reddens the named rows + link."""

    def __init__(self, sql, size=22, **kw):
        super().__init__(**kw)
        self.t = Text(sql, font="PT Mono", font_size=size, color=INK)
        self.add(self.t)

    def type_in(self, scene, total=1.6):
        scene.play(AddTextLetterByLetter(self.t, time_per_char=max(0.01, total / max(1, len(self.t.text)))))

    @staticmethod
    def highlight_join(scene, rows, lines, total=0.8):
        scene.play(*[r.animate.set_color(RED) for r in rows], *[l.animate.set_stroke(RED, 3.5) for l in lines],
                   run_time=total)


# ── 3. DataPipeline ──────────────────────────────────────────────────────────
class DataPipeline:
    """messy rows → clean table → line chart → named outputs. Numbers are NEVER shown unless
    the article gives them — the chart is a schematic shape with no axis units."""

    def __init__(self, n_rows=7, outputs=("output one", "output two", "output three")):
        self.n, self.outputs = n_rows, outputs

    def play(self, scene, total=12.0):
        n = self.n
        # 1. messy rows (jittered gray bars) on the left
        rows = VGroup()
        rng = np.random.default_rng(7)
        for i in range(n):
            w = 1.2 + rng.random() * 1.6
            r = Rectangle(width=w, height=0.22, stroke_width=0, fill_color=GRAY, fill_opacity=0.55)
            r.move_to(LEFT * 5.5 + UP * (1.3 - i * 0.55) + RIGHT * (rng.random() * 0.6))
            rows.add(r)
        cap1 = T("raw ride records", 20, GRAY).next_to(rows, UP, buff=0.3)
        scene.play(LaggedStart(*[FadeIn(r, shift=LEFT * 0.2) for r in rows], lag_ratio=0.08), FadeIn(cap1), run_time=total * 0.16)
        # 2. clean into a table (aligned rows, hairline grid)
        tbl = VGroup()
        for i in range(n):
            r = Rectangle(width=2.6, height=0.3, stroke_color=HAIR, stroke_width=1.5, fill_color=LIGHT, fill_opacity=1)
            r.move_to(LEFT * 2.1 + UP * (1.3 - i * 0.46))
            tbl.add(r)
        cap2 = T("cleaned · processed", 20, GRAY).next_to(tbl, UP, buff=0.3)
        arrow1 = Arrow(rows.get_right() + RIGHT * 0.1, tbl.get_left() + LEFT * 0.1, buff=0.1, stroke_width=3, color=GRAY)
        scene.play(Create(arrow1), run_time=total * 0.05)
        scene.play(*[Transform(rows[i], tbl[i]) for i in range(n)], FadeIn(cap2), run_time=total * 0.16)
        # 3. a schematic demand curve draws (no units — none in the article)
        ax = Axes(x_range=[0, 10, 10], y_range=[0, 6, 6], x_length=3.4, y_length=3.0,
                  axis_config={"stroke_color": GRAY, "stroke_width": 2, "include_ticks": False, "include_tip": False})
        ax.move_to(RIGHT * 0.9 + DOWN * 0.3)
        pts = [ax.c2p(x, y) for x, y in [(0, 1.2), (1.5, 1.6), (3, 3.8), (4.5, 2.4), (6, 4.6), (7.5, 5.2), (9, 2.9), (10, 2.2)]]
        curve = VMobject(stroke_color=RED, stroke_width=4).set_points_smoothly(pts)
        cap3 = T("patterns · trends", 20, GRAY).next_to(ax, UP, buff=0.2)
        arrow2 = Arrow(tbl.get_right() + RIGHT * 0.1, ax.get_left() + LEFT * 0.1, buff=0.1, stroke_width=3, color=GRAY)
        scene.play(Create(arrow2), run_time=total * 0.05)
        scene.play(Create(ax), FadeIn(cap3), run_time=total * 0.10)
        scene.play(Create(curve), run_time=total * 0.16)
        # 4. outputs branch off the chart
        outs = VGroup(*[T(o, 22) for o in self.outputs]).arrange(DOWN, buff=0.7, aligned_edge=LEFT)
        outs.next_to(ax, RIGHT, buff=0.55).align_to(ax, UP)
        tip = curve.get_end()
        branches = VGroup(*[Line(tip, o.get_left() + LEFT * 0.12, stroke_width=2, color=GRAY) for o in outs])
        scene.play(LaggedStart(*[AnimationGroup(Create(b), FadeIn(o, shift=RIGHT * 0.15)) for b, o in zip(branches, outs)],
                               lag_ratio=0.35), run_time=total * 0.22)
