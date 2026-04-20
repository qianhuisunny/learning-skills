#!/usr/bin/env python3
"""
eLearning Storyboard Template — Dark EY Theme
Reusable python-pptx module for generating storyboard cards.

STYLE RULES:
- Sentence case everywhere (not title case)
- Body content starts at same left margin as title
- Pop-ups have WHITE background panels overlaying the dark slide
- Content inside pop-ups uses CHARCOAL text on white

Usage:
    from storyboard_template import StoryboardBuilder
    sb = StoryboardBuilder("Module 2.5 — Developing the procurement plan")
    sb.add_title_slide("Module 2.5", "Developing the procurement plan", "Subtitle")
    sb.add_anchor("2.5-2", "Title", tiles=[...])
    sb.add_popup_text("2.5-2-01", "Anchor title", 1, "Component name", ...)
    sb.save("/path/to/output.pptx")
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE


# ── Dark EY Theme Constants ─────────────────────────────────────
BG_COLOR        = RGBColor(0x1C, 0x23, 0x33)
TITLE_BLUE      = RGBColor(0x1A, 0x9A, 0xFA)   # EY-Parthenon #1A9AFA
COMPONENT_BLUE  = RGBColor(0x1A, 0x9A, 0xFA)   # EY-Parthenon #1A9AFA
DARK_BLUE       = RGBColor(0x12, 0x6E, 0xB3)   # Darker shade for number badges
GREEN_BULLET    = RGBColor(0x7A, 0xB6, 0x48)
SUCCESS_GREEN   = RGBColor(0x27, 0xAE, 0x60)
ERROR_RED       = RGBColor(0xC0, 0x39, 0x2B)
WHITE           = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT_GRAY      = RGBColor(0xAA, 0xAA, 0xAA)
MED_GRAY        = RGBColor(0x7F, 0x8C, 0x8D)
FOOTER_GRAY     = RGBColor(0x88, 0x88, 0x88)
BORDER_BLUE     = RGBColor(0x1A, 0x9A, 0xFA)   # EY-Parthenon #1A9AFA
BORDER_LIGHT    = RGBColor(0xD5, 0xD8, 0xDC)
YELLOW_ACCENT   = RGBColor(0xFF, 0xE6, 0x00)
PANEL_BG        = RGBColor(0x25, 0x30, 0x45)
CHARCOAL        = RGBColor(0x2C, 0x3E, 0x50)
DARK_GRAY       = RGBColor(0x4A, 0x4A, 0x4A)
FAINT_GRAY      = RGBColor(0xF4, 0xF6, 0xF7)

FONT_TITLE = "Calibri"
FONT_BODY  = "Calibri"

SLIDE_WIDTH  = Inches(13.333)
SLIDE_HEIGHT = Inches(7.5)

LEFT_MARGIN   = Inches(0.7)
CONTENT_WIDTH = Inches(11.9)

# Pop-up white panel geometry
POPUP_PANEL_TOP    = Inches(1.15)
POPUP_PANEL_LEFT   = Inches(0.4)
POPUP_PANEL_WIDTH  = Inches(12.5)
POPUP_PANEL_HEIGHT = Inches(5.8)
POPUP_PANEL_BOTTOM = POPUP_PANEL_TOP + POPUP_PANEL_HEIGHT

# Inside the white panel, content margins
POPUP_CONTENT_LEFT = Inches(0.7)
POPUP_CONTENT_WIDTH = Inches(11.5)
POPUP_BAR_TOP      = POPUP_PANEL_TOP + Inches(0.1)
POPUP_CONTENT_TOP  = POPUP_PANEL_TOP + Inches(0.8)


class StoryboardBuilder:
    """Builds a storyboard PowerPoint in the dark EY theme."""

    def __init__(self, module_name="eLearning module", date_str="12 March 2026"):
        self.prs = Presentation()
        self.prs.slide_width = SLIDE_WIDTH
        self.prs.slide_height = SLIDE_HEIGHT
        self.module_name = module_name
        self.date_str = date_str
        self.slide_count = 0

    # ── Private helpers ──────────────────────────────────────────

    def _new_slide(self):
        slide = self.prs.slides.add_slide(self.prs.slide_layouts[6])
        bg = slide.background.fill
        bg.solid()
        bg.fore_color.rgb = BG_COLOR
        self.slide_count += 1
        return slide

    def _add_footer(self, slide):
        num = self.slide_count
        tb = slide.shapes.add_textbox(Inches(0.3), Inches(7.05), Inches(0.4), Pt(18))
        p = tb.text_frame.paragraphs[0]
        p.text = str(num)
        p.font.size = Pt(9)
        p.font.color.rgb = FOOTER_GRAY
        p.font.name = FONT_BODY
        tb = slide.shapes.add_textbox(Inches(0.8), Inches(7.05), Inches(1.5), Pt(18))
        p = tb.text_frame.paragraphs[0]
        p.text = self.date_str
        p.font.size = Pt(9)
        p.font.color.rgb = FOOTER_GRAY
        p.font.name = FONT_BODY
        tb = slide.shapes.add_textbox(Inches(3.5), Inches(7.05), Inches(6.5), Pt(18))
        p = tb.text_frame.paragraphs[0]
        p.text = f"Internal use only  |  {self.module_name}"
        p.font.size = Pt(9)
        p.font.color.rgb = FOOTER_GRAY
        p.font.name = FONT_BODY
        p.alignment = PP_ALIGN.CENTER

    def _add_slide_title(self, slide, text, size=Pt(32)):
        tb = slide.shapes.add_textbox(LEFT_MARGIN, Inches(0.4), Inches(12), Pt(50))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = text
        p.font.size = size
        p.font.color.rgb = TITLE_BLUE
        p.font.bold = True
        p.font.name = FONT_TITLE

    def _add_layout_badge(self, slide, slide_num, layout_id):
        tb = slide.shapes.add_textbox(Inches(10.5), Inches(0.4), Inches(2.5), Pt(25))
        tf = tb.text_frame
        p = tf.paragraphs[0]
        p.text = f"{slide_num}  |  {layout_id}"
        p.font.size = Pt(12)
        p.font.color.rgb = LIGHT_GRAY
        p.font.bold = True
        p.font.name = FONT_BODY
        p.alignment = PP_ALIGN.RIGHT

    def _add_speaker_notes(self, slide, notes):
        slide.notes_slide.notes_text_frame.text = notes

    def _add_section_label(self, slide, text, left, top, width=Inches(4),
                           color=YELLOW_ACCENT):
        tb = slide.shapes.add_textbox(left, top, width, Pt(18))
        p = tb.text_frame.paragraphs[0]
        p.text = text
        p.font.size = Pt(10)
        p.font.color.rgb = color
        p.font.bold = True
        p.font.name = FONT_BODY

    def _add_content_box(self, slide, left, top, width, height,
                         fill_color=PANEL_BG, border_color=BORDER_BLUE):
        box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
        box.fill.solid()
        box.fill.fore_color.rgb = fill_color
        box.line.color.rgb = border_color
        box.line.width = Pt(1)
        return box

    def _add_text(self, slide, text, left, top, width, height,
                  size=Pt(16), color=WHITE, bold=False, align=PP_ALIGN.LEFT):
        tb = slide.shapes.add_textbox(left, top, width, height)
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = text
        p.font.size = size
        p.font.color.rgb = color
        p.font.bold = bold
        p.font.name = FONT_BODY
        p.alignment = align
        p.line_spacing = Pt(size.pt * 1.5)
        return tf

    def _add_bullets(self, slide, items, left, top, width, height,
                     size=Pt(15), bullet_color=GREEN_BULLET, text_color=WHITE):
        tb = slide.shapes.add_textbox(left, top, width, height)
        tf = tb.text_frame
        tf.word_wrap = True
        for i, item in enumerate(items):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            r1 = p.add_run()
            r1.text = "\u25CF  "
            r1.font.size = Pt(12)
            r1.font.color.rgb = bullet_color
            r1.font.name = FONT_BODY
            r2 = p.add_run()
            r2.text = item
            r2.font.size = size
            r2.font.color.rgb = text_color
            r2.font.name = FONT_BODY
            p.space_after = Pt(10)
            p.line_spacing = Pt(24)
        return tf

    def _add_check_bullets(self, slide, items, left, top, width, height,
                           size=Pt(15), check_color=COMPONENT_BLUE,
                           text_color=CHARCOAL):
        """Checkmark bullets — used inside white pop-up panels."""
        tb = slide.shapes.add_textbox(left, top, width, height)
        tf = tb.text_frame
        tf.word_wrap = True
        for i, item in enumerate(items):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            r1 = p.add_run()
            r1.text = "\u2713  "
            r1.font.size = Pt(14)
            r1.font.color.rgb = check_color
            r1.font.name = FONT_BODY
            r2 = p.add_run()
            r2.text = item
            r2.font.size = size
            r2.font.color.rgb = text_color
            r2.font.name = FONT_BODY
            p.space_after = Pt(10)
            p.line_spacing = Pt(24)
        return tf

    def _add_media_placeholder(self, slide, label, left, top, width, height,
                               on_white=False):
        fill = WHITE if on_white else PANEL_BG
        border = BORDER_LIGHT if on_white else BORDER_BLUE
        self._add_content_box(slide, left, top, width, height,
                              fill_color=fill, border_color=border)
        txt_color = MED_GRAY if on_white else LIGHT_GRAY
        self._add_text(slide, label, left + Inches(0.2), top + Inches(0.2),
                       width - Inches(0.4), height - Inches(0.4),
                       size=Pt(13), color=txt_color, align=PP_ALIGN.CENTER)

    def _format_notes(self, vo="", visual="", interaction=""):
        parts = []
        if vo:
            parts.append(f"VOICEOVER:\n{vo}")
        if visual:
            parts.append(f"VISUAL/GRAPHIC DESCRIPTION:\n{visual}")
        if interaction:
            parts.append(f"INTERACTION & DEV NOTES:\n{interaction}")
        return "\n\n".join(parts)

    def _format_feedback_notes(self, vo="", correct="", incorrect="", dev=""):
        parts = []
        if vo:
            parts.append(f"VOICEOVER:\n{vo}")
        if correct:
            parts.append(f"FEEDBACK — CORRECT:\n{correct}")
        if incorrect:
            parts.append(f"FEEDBACK — INCORRECT:\n{incorrect}")
        if dev:
            parts.append(f"DEV NOTES:\n{dev}")
        return "\n\n".join(parts)

    # ── Pop-up panel helpers ─────────────────────────────────────

    def _add_popup_white_panel(self, slide):
        """Draw the large white rectangle that IS the pop-up."""
        panel = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE,
            POPUP_PANEL_LEFT, POPUP_PANEL_TOP,
            POPUP_PANEL_WIDTH, POPUP_PANEL_HEIGHT)
        panel.fill.solid()
        panel.fill.fore_color.rgb = WHITE
        panel.line.fill.background()
        return panel

    def _add_popup_header(self, slide, comp_num, comp_title):
        """Component bar with number badge and X close, at top of white panel."""
        bar_y = POPUP_BAR_TOP
        bar_h = Inches(0.5)
        bar_x = POPUP_PANEL_LEFT + Inches(0.15)
        bar_w = POPUP_PANEL_WIDTH - Inches(0.3)
        # Bar background
        bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,
                                     bar_x, bar_y, bar_w, bar_h)
        bar.fill.solid()
        bar.fill.fore_color.rgb = COMPONENT_BLUE
        bar.line.fill.background()
        # Number badge
        badge_w = Inches(0.5)
        badge = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,
                                       bar_x, bar_y, badge_w, bar_h)
        badge.fill.solid()
        badge.fill.fore_color.rgb = DARK_BLUE
        badge.line.fill.background()
        self._add_text(slide, f"{comp_num:02d}", bar_x, bar_y,
                       badge_w, bar_h, size=Pt(15),
                       color=WHITE, bold=True, align=PP_ALIGN.CENTER)
        # Title text
        self._add_text(slide, comp_title,
                       bar_x + badge_w + Inches(0.15), bar_y,
                       bar_w - badge_w - Inches(1), bar_h,
                       size=Pt(14), color=WHITE, bold=True)
        # X close button
        x_btn = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,
                                       bar_x + bar_w - Inches(0.5),
                                       bar_y, Inches(0.5), bar_h)
        x_btn.fill.solid()
        x_btn.fill.fore_color.rgb = DARK_BLUE
        x_btn.line.fill.background()
        self._add_text(slide, "\u2715",
                       bar_x + bar_w - Inches(0.5), bar_y,
                       Inches(0.5), bar_h,
                       size=Pt(16), color=WHITE, bold=True, align=PP_ALIGN.CENTER)

    # ── Public: Title Slide ──────────────────────────────────────

    def add_title_slide(self, module_num, title, subtitle=""):
        slide = self._new_slide()
        bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,
                                     Inches(0), Inches(0), SLIDE_WIDTH, Inches(0.06))
        bar.fill.solid()
        bar.fill.fore_color.rgb = YELLOW_ACCENT
        bar.line.fill.background()
        self._add_text(slide, module_num.upper(), LEFT_MARGIN, Inches(2.2),
                       Inches(10), Pt(30), size=Pt(18), color=LIGHT_GRAY, bold=True)
        self._add_text(slide, title, LEFT_MARGIN, Inches(2.8),
                       Inches(10), Inches(1.2), size=Pt(44), color=WHITE, bold=True)
        if subtitle:
            self._add_text(slide, subtitle, LEFT_MARGIN, Inches(4.2),
                           Inches(10), Pt(30), size=Pt(18), color=LIGHT_GRAY)
        self._add_footer(slide)
        return slide

    # ── Public: Layout L01 — 1C Text ────────────────────────────

    def add_L01(self, slide_num, title, body, bullets=None, notes=""):
        slide = self._new_slide()
        self._add_slide_title(slide, title)
        self._add_layout_badge(slide, slide_num, "L01")
        self._add_text(slide, body, LEFT_MARGIN, Inches(1.4),
                       CONTENT_WIDTH, Inches(2), size=Pt(18))
        if bullets:
            self._add_bullets(slide, bullets, LEFT_MARGIN, Inches(3.0),
                              CONTENT_WIDTH, Inches(3.5))
        if notes:
            self._add_speaker_notes(slide, notes)
        self._add_footer(slide)
        return slide

    # ── Public: Layout L02 — 1C Hero + Body ─────────────────────

    def add_L02(self, slide_num, title, hero_label, body, cta=None, notes=""):
        slide = self._new_slide()
        self._add_slide_title(slide, title)
        self._add_layout_badge(slide, slide_num, "L02")
        self._add_media_placeholder(slide, hero_label, LEFT_MARGIN, Inches(1.3),
                                    CONTENT_WIDTH, Inches(3))
        self._add_text(slide, body, LEFT_MARGIN, Inches(4.6),
                       CONTENT_WIDTH, Inches(1.5), size=Pt(18))
        if cta:
            btn = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                                         Inches(10.5), Inches(6.2), Inches(2), Inches(0.5))
            btn.fill.solid()
            btn.fill.fore_color.rgb = COMPONENT_BLUE
            btn.line.fill.background()
            self._add_text(slide, cta, Inches(10.5), Inches(6.2),
                           Inches(2), Inches(0.5), size=Pt(14),
                           color=WHITE, bold=True, align=PP_ALIGN.CENTER)
        if notes:
            self._add_speaker_notes(slide, notes)
        self._add_footer(slide)
        return slide

    # ── Public: Layout L03 — 2C 60/40 (Media Left) ──────────────

    def add_L03(self, slide_num, title, media_label, heading, body,
                bullets=None, notes=""):
        slide = self._new_slide()
        self._add_slide_title(slide, title)
        self._add_layout_badge(slide, slide_num, "L03")
        self._add_media_placeholder(slide, media_label, LEFT_MARGIN, Inches(1.4),
                                    Inches(7), Inches(4.8))
        rx = Inches(8.0)
        rw = Inches(4.8)
        self._add_text(slide, heading, rx, Inches(1.4), rw, Pt(30),
                       size=Pt(20), color=WHITE, bold=True)
        self._add_text(slide, body, rx, Inches(2.0), rw, Inches(2), size=Pt(16))
        if bullets:
            self._add_bullets(slide, bullets, rx, Inches(3.5), rw, Inches(3))
        if notes:
            self._add_speaker_notes(slide, notes)
        self._add_footer(slide)
        return slide

    # ── Public: Layout L04 — 2C 40/60 (Media Right) ─────────────

    def add_L04(self, slide_num, title, heading, body, media_label,
                bullets=None, notes=""):
        slide = self._new_slide()
        self._add_slide_title(slide, title)
        self._add_layout_badge(slide, slide_num, "L04")
        lw = Inches(4.8)
        self._add_text(slide, heading, LEFT_MARGIN, Inches(1.4), lw, Pt(30),
                       size=Pt(20), color=WHITE, bold=True)
        self._add_text(slide, body, LEFT_MARGIN, Inches(2.0), lw, Inches(2), size=Pt(16))
        if bullets:
            self._add_bullets(slide, bullets, LEFT_MARGIN, Inches(3.5), lw, Inches(3))
        self._add_media_placeholder(slide, media_label, Inches(5.8), Inches(1.4),
                                    Inches(7), Inches(4.8))
        if notes:
            self._add_speaker_notes(slide, notes)
        self._add_footer(slide)
        return slide

    # ── Public: Layout L05 — 3-up Cards ──────────────────────────

    def add_L05(self, slide_num, title, cards, notes=""):
        """cards: list of (icon_label, heading, body) tuples, max 3."""
        slide = self._new_slide()
        self._add_slide_title(slide, title)
        self._add_layout_badge(slide, slide_num, "L05")
        card_w = Inches(3.7)
        gap = Inches(0.4)
        for i, (icon, heading, body) in enumerate(cards[:3]):
            x = LEFT_MARGIN + i * (card_w + gap)
            y = Inches(1.8)
            self._add_content_box(slide, x, y, card_w, Inches(4))
            self._add_text(slide, icon, x, y + Inches(0.3), card_w, Pt(20),
                           size=Pt(12), color=LIGHT_GRAY, align=PP_ALIGN.CENTER)
            self._add_text(slide, heading, x + Inches(0.2), y + Inches(1.0),
                           card_w - Inches(0.4), Pt(30),
                           size=Pt(18), color=WHITE, bold=True, align=PP_ALIGN.CENTER)
            self._add_text(slide, body, x + Inches(0.2), y + Inches(1.8),
                           card_w - Inches(0.4), Inches(2),
                           size=Pt(14), color=LIGHT_GRAY, align=PP_ALIGN.CENTER)
        if notes:
            self._add_speaker_notes(slide, notes)
        self._add_footer(slide)
        return slide

    # ── Public: Layout L06 — Compare 2-up ────────────────────────

    def add_L06(self, slide_num, title, col_a_header, col_a_items,
                col_b_header, col_b_items, notes=""):
        slide = self._new_slide()
        self._add_slide_title(slide, title)
        self._add_layout_badge(slide, slide_num, "L06")
        col_w = Inches(5.8)
        ax = LEFT_MARGIN
        self._add_content_box(slide, ax, Inches(1.6), col_w, Inches(0.5))
        self._add_text(slide, col_a_header, ax + Inches(0.2), Inches(1.6),
                       col_w, Inches(0.5), size=Pt(16), color=WHITE, bold=True)
        self._add_bullets(slide, col_a_items, ax + Inches(0.2), Inches(2.3),
                          col_w - Inches(0.4), Inches(4))
        bx = Inches(6.8)
        self._add_content_box(slide, bx, Inches(1.6), col_w, Inches(0.5))
        self._add_text(slide, col_b_header, bx + Inches(0.2), Inches(1.6),
                       col_w, Inches(0.5), size=Pt(16), color=WHITE, bold=True)
        self._add_bullets(slide, col_b_items, bx + Inches(0.2), Inches(2.3),
                          col_w - Inches(0.4), Inches(4))
        if notes:
            self._add_speaker_notes(slide, notes)
        self._add_footer(slide)
        return slide

    # ── Public: Layout L07 — Stepper (1→N) ──────────────────────

    def add_L07(self, slide_num, title, steps, notes=""):
        """steps: list of (label, caption) tuples."""
        slide = self._new_slide()
        self._add_slide_title(slide, title)
        self._add_layout_badge(slide, slide_num, "L07")
        n = len(steps)
        step_w = Inches(2.2)
        total_w = n * step_w + (n - 1) * Inches(0.8)
        start_x = LEFT_MARGIN
        y_circle = Inches(2.5)
        for i, (label, caption) in enumerate(steps):
            x = start_x + i * (step_w + Inches(0.8))
            circle = slide.shapes.add_shape(MSO_SHAPE.OVAL,
                                            x + Inches(0.9), y_circle,
                                            Inches(0.5), Inches(0.5))
            circle.fill.solid()
            circle.fill.fore_color.rgb = COMPONENT_BLUE
            circle.line.fill.background()
            self._add_text(slide, str(i + 1), x + Inches(0.9), y_circle,
                           Inches(0.5), Inches(0.5), size=Pt(16),
                           color=WHITE, bold=True, align=PP_ALIGN.CENTER)
            if i < n - 1:
                arrow = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW,
                                               x + Inches(1.5), y_circle + Inches(0.1),
                                               Inches(0.7), Inches(0.3))
                arrow.fill.solid()
                arrow.fill.fore_color.rgb = LIGHT_GRAY
                arrow.line.fill.background()
            self._add_text(slide, label, x, y_circle + Inches(0.7),
                           step_w, Pt(25), size=Pt(16),
                           color=WHITE, bold=True, align=PP_ALIGN.CENTER)
            self._add_text(slide, caption, x, y_circle + Inches(1.2),
                           step_w, Inches(1.5), size=Pt(13),
                           color=LIGHT_GRAY, align=PP_ALIGN.CENTER)
        if notes:
            self._add_speaker_notes(slide, notes)
        self._add_footer(slide)
        return slide

    # ── Public: Layout L08 — Timeline ────────────────────────────

    def add_L08(self, slide_num, title, nodes, notes=""):
        """nodes: list of (date_label, content) tuples."""
        slide = self._new_slide()
        self._add_slide_title(slide, title)
        self._add_layout_badge(slide, slide_num, "L08")
        line_x = Inches(3.0)
        start_y = Inches(1.8)
        gap = Inches(1.1)
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,
                                      line_x, start_y,
                                      Pt(2), Inches(len(nodes) * 1.1))
        line.fill.solid()
        line.fill.fore_color.rgb = BORDER_BLUE
        line.line.fill.background()
        for i, (date_label, content) in enumerate(nodes):
            y = start_y + i * gap
            circle = slide.shapes.add_shape(MSO_SHAPE.OVAL,
                                            line_x - Inches(0.1), y,
                                            Inches(0.25), Inches(0.25))
            circle.fill.solid()
            circle.fill.fore_color.rgb = COMPONENT_BLUE
            circle.line.fill.background()
            self._add_text(slide, date_label, LEFT_MARGIN, y,
                           Inches(2), Pt(20), size=Pt(14),
                           color=YELLOW_ACCENT, bold=True, align=PP_ALIGN.RIGHT)
            self._add_text(slide, content, Inches(3.5), y,
                           Inches(8), Inches(0.8), size=Pt(15))
        if notes:
            self._add_speaker_notes(slide, notes)
        self._add_footer(slide)
        return slide

    # ── Public: Layout L09 — MCQ (Default State) ────────────────

    def add_L09_default(self, slide_num, title, stem, options, notes=""):
        slide = self._new_slide()
        self._add_slide_title(slide, title)
        self._add_layout_badge(slide, slide_num, "L09")
        self._add_text(slide, stem, LEFT_MARGIN, Inches(1.5),
                       CONTENT_WIDTH, Inches(1), size=Pt(18), bold=True)
        y = Inches(2.8)
        for i, opt in enumerate(options):
            letter = chr(65 + i)
            tb = slide.shapes.add_textbox(LEFT_MARGIN + Inches(0.3), y, Inches(10), Pt(30))
            tf = tb.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            r1 = p.add_run()
            r1.text = f"\u25CB  {letter}.  "
            r1.font.size = Pt(16)
            r1.font.color.rgb = COMPONENT_BLUE
            r1.font.name = FONT_BODY
            r2 = p.add_run()
            r2.text = opt
            r2.font.size = Pt(16)
            r2.font.color.rgb = WHITE
            r2.font.name = FONT_BODY
            y += Inches(0.6)
        btn = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                                     Inches(10.5), Inches(6.0), Inches(2), Inches(0.5))
        btn.fill.solid()
        btn.fill.fore_color.rgb = COMPONENT_BLUE
        btn.line.fill.background()
        self._add_text(slide, "Submit", Inches(10.5), Inches(6.0),
                       Inches(2), Inches(0.5), size=Pt(14),
                       color=WHITE, bold=True, align=PP_ALIGN.CENTER)
        if notes:
            self._add_speaker_notes(slide, notes)
        self._add_footer(slide)
        return slide

    # ── Public: Layout L09 — MCQ (Feedback State) ───────────────

    def add_L09_feedback(self, slide_num, title, stem, options, correct_idx,
                         feedback_correct, feedback_incorrect, notes=""):
        slide = self._new_slide()
        self._add_slide_title(slide, title)
        self._add_layout_badge(slide, slide_num, "L09 — Feedback")
        lw = Inches(8.2)
        self._add_text(slide, stem, LEFT_MARGIN, Inches(1.5),
                       lw, Inches(1), size=Pt(18), bold=True)
        y = Inches(2.8)
        for i, opt in enumerate(options):
            letter = chr(65 + i)
            is_correct = (i == correct_idx)
            tb = slide.shapes.add_textbox(LEFT_MARGIN + Inches(0.3), y, Inches(7), Pt(30))
            tf = tb.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            r1 = p.add_run()
            r1.text = f"\u25C9  {letter}.  " if is_correct else f"\u25CB  {letter}.  "
            r1.font.size = Pt(16)
            r1.font.color.rgb = SUCCESS_GREEN if is_correct else LIGHT_GRAY
            r1.font.name = FONT_BODY
            r2 = p.add_run()
            r2.text = opt
            r2.font.size = Pt(16)
            r2.font.color.rgb = WHITE
            r2.font.name = FONT_BODY
            y += Inches(0.6)
        panel_x = Inches(8.8)
        panel_w = Inches(4.2)
        self._add_content_box(slide, panel_x, Inches(1.2), panel_w, Inches(2.3))
        self._add_section_label(slide, "\u2713 CORRECT", panel_x + Inches(0.2), Inches(1.35))
        self._add_text(slide, feedback_correct, panel_x + Inches(0.2), Inches(1.7),
                       panel_w - Inches(0.4), Inches(1.5), size=Pt(14))
        self._add_content_box(slide, panel_x, Inches(3.7), panel_w, Inches(2.3))
        self._add_section_label(slide, "\u2717 INCORRECT", panel_x + Inches(0.2), Inches(3.85))
        self._add_text(slide, feedback_incorrect, panel_x + Inches(0.2), Inches(4.2),
                       panel_w - Inches(0.4), Inches(1.5), size=Pt(14))
        btn = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                                     panel_x + Inches(1.0), Inches(6.2),
                                     Inches(2), Inches(0.5))
        btn.fill.solid()
        btn.fill.fore_color.rgb = COMPONENT_BLUE
        btn.line.fill.background()
        self._add_text(slide, "Continue", panel_x + Inches(1.0), Inches(6.2),
                       Inches(2), Inches(0.5), size=Pt(14),
                       color=WHITE, bold=True, align=PP_ALIGN.CENTER)
        if notes:
            self._add_speaker_notes(slide, notes)
        self._add_footer(slide)
        return slide

    # ── Public: Layout L10 — Scenario Choice (Default) ──────────

    def add_L10_default(self, slide_num, title, context, choices, notes=""):
        slide = self._new_slide()
        self._add_slide_title(slide, title)
        self._add_layout_badge(slide, slide_num, "L10")
        self._add_content_box(slide, LEFT_MARGIN, Inches(1.3), CONTENT_WIDTH, Inches(2.2))
        self._add_section_label(slide, "SCENARIO", LEFT_MARGIN + Inches(0.2), Inches(1.4))
        self._add_text(slide, context, LEFT_MARGIN + Inches(0.2), Inches(1.8),
                       CONTENT_WIDTH - Inches(0.4), Inches(1.5), size=Pt(16))
        n = len(choices)
        btn_w = Inches(3.5)
        gap = Inches(0.5)
        total = n * btn_w + (n - 1) * gap
        start_x = LEFT_MARGIN
        for i, choice in enumerate(choices):
            x = start_x + i * (btn_w + gap)
            btn = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                                         x, Inches(4.2), btn_w, Inches(1.2))
            btn.fill.solid()
            btn.fill.fore_color.rgb = PANEL_BG
            btn.line.color.rgb = BORDER_BLUE
            btn.line.width = Pt(1)
            self._add_text(slide, choice, x + Inches(0.2), Inches(4.3),
                           btn_w - Inches(0.4), Inches(1),
                           size=Pt(15), align=PP_ALIGN.CENTER)
        if notes:
            self._add_speaker_notes(slide, notes)
        self._add_footer(slide)
        return slide

    # ── Public: Layout L10 — Scenario Choice (Feedback) ─────────

    def add_L10_feedback(self, slide_num, title, context, chosen,
                         consequence, notes=""):
        slide = self._new_slide()
        self._add_slide_title(slide, title)
        self._add_layout_badge(slide, slide_num, "L10 — Feedback")
        lw = Inches(8.2)
        self._add_content_box(slide, LEFT_MARGIN, Inches(1.3), lw, Inches(2.2))
        self._add_section_label(slide, "SCENARIO", LEFT_MARGIN + Inches(0.2), Inches(1.4))
        self._add_text(slide, context, LEFT_MARGIN + Inches(0.2), Inches(1.8),
                       lw - Inches(0.4), Inches(1.5), size=Pt(16))
        self._add_section_label(slide, "SELECTED", LEFT_MARGIN + Inches(0.2), Inches(3.8))
        self._add_text(slide, chosen, LEFT_MARGIN + Inches(0.2), Inches(4.2),
                       lw - Inches(0.4), Inches(1), size=Pt(16), bold=True)
        panel_x = Inches(8.8)
        panel_w = Inches(4.2)
        self._add_content_box(slide, panel_x, Inches(1.2), panel_w, Inches(5))
        self._add_section_label(slide, "CONSEQUENCE", panel_x + Inches(0.2), Inches(1.35))
        self._add_text(slide, consequence, panel_x + Inches(0.2), Inches(1.8),
                       panel_w - Inches(0.4), Inches(4), size=Pt(15))
        btn = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                                     panel_x + Inches(1.0), Inches(6.2),
                                     Inches(2), Inches(0.5))
        btn.fill.solid()
        btn.fill.fore_color.rgb = COMPONENT_BLUE
        btn.line.fill.background()
        self._add_text(slide, "Continue", panel_x + Inches(1.0), Inches(6.2),
                       Inches(2), Inches(0.5), size=Pt(14),
                       color=WHITE, bold=True, align=PP_ALIGN.CENTER)
        if notes:
            self._add_speaker_notes(slide, notes)
        self._add_footer(slide)
        return slide

    # ── Public: Layout L11 — Drag/Match (Default) ───────────────

    def add_L11_default(self, slide_num, title, instruction, items, targets, notes=""):
        slide = self._new_slide()
        self._add_slide_title(slide, title)
        self._add_layout_badge(slide, slide_num, "L11")
        self._add_content_box(slide, LEFT_MARGIN, Inches(1.3), CONTENT_WIDTH, Inches(0.5))
        self._add_text(slide, instruction, LEFT_MARGIN + Inches(0.2), Inches(1.3),
                       CONTENT_WIDTH - Inches(0.4), Inches(0.5), size=Pt(14), bold=True)
        self._add_section_label(slide, "DRAG ITEMS", LEFT_MARGIN, Inches(2.1))
        y = Inches(2.5)
        for item in items:
            self._add_content_box(slide, LEFT_MARGIN, y, Inches(4.5), Inches(0.55))
            self._add_text(slide, item, LEFT_MARGIN + Inches(0.2), y,
                           Inches(4.1), Inches(0.55), size=Pt(14))
            y += Inches(0.7)
        self._add_section_label(slide, "DROP TARGETS", Inches(5.8), Inches(2.1))
        y = Inches(2.5)
        for target in targets:
            box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,
                                         Inches(5.8), y, Inches(7), Inches(0.55))
            box.fill.solid()
            box.fill.fore_color.rgb = BG_COLOR
            box.line.color.rgb = LIGHT_GRAY
            box.line.width = Pt(1)
            self._add_text(slide, target, Inches(6.0), y,
                           Inches(6.6), Inches(0.55), size=Pt(14), color=LIGHT_GRAY)
            y += Inches(0.7)
        if notes:
            self._add_speaker_notes(slide, notes)
        self._add_footer(slide)
        return slide

    # ── Public: Anchor Slide (L12 Menu Grid) ─────────────────────

    def _build_anchor_grid(self, slide, slide_num, title, subtitle, tiles,
                           visited=None):
        self._add_slide_title(slide, title)
        badge_label = "L12" if not visited else "L12 — Visited"
        self._add_layout_badge(slide, slide_num, badge_label)
        if subtitle:
            tb = slide.shapes.add_textbox(LEFT_MARGIN, Inches(1.0), Inches(10), Pt(22))
            tf = tb.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            p.text = subtitle
            p.font.size = Pt(13)
            p.font.color.rgb = LIGHT_GRAY
            p.font.italic = True
            p.font.name = FONT_BODY
        visited = visited or set()
        n = len(tiles)
        cols = min(n, 4)
        tile_w = Inches(2.8)
        tile_h = Inches(1.0)
        gap_x = Inches(0.35)
        gap_y = Inches(0.3)
        # Align grid to LEFT_MARGIN, same as title
        start_x = LEFT_MARGIN
        start_y = Inches(1.6)
        for i, (icon, label) in enumerate(tiles):
            col = i % cols
            row = i // cols
            x = start_x + col * (tile_w + gap_x)
            y = start_y + row * (tile_h + gap_y)
            bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, tile_w, tile_h)
            bar.fill.solid()
            bar.fill.fore_color.rgb = COMPONENT_BLUE
            bar.line.fill.background()
            badge = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,
                                           x, y, Inches(0.5), tile_h)
            badge.fill.solid()
            badge.fill.fore_color.rgb = DARK_BLUE
            badge.line.fill.background()
            self._add_text(slide, f"{i+1:02d}", x, y, Inches(0.5), tile_h,
                           size=Pt(14), color=WHITE, bold=True, align=PP_ALIGN.CENTER)
            self._add_text(slide, label, x + Inches(0.6), y,
                           tile_w - Inches(0.7), tile_h,
                           size=Pt(12), color=WHITE, bold=True)
            if i in visited:
                self._add_text(slide, "\u2713", x + tile_w - Inches(0.4), y,
                               Inches(0.35), tile_h,
                               size=Pt(18), color=SUCCESS_GREEN, bold=True,
                               align=PP_ALIGN.CENTER)

    def add_anchor(self, slide_num, title, tiles, subtitle="", notes=""):
        slide = self._new_slide()
        self._build_anchor_grid(slide, slide_num, title, subtitle, tiles)
        if notes:
            self._add_speaker_notes(slide, notes)
        self._add_footer(slide)
        return slide

    def add_anchor_visited(self, slide_num, title, tiles, visited=None,
                           subtitle="", notes=""):
        slide = self._new_slide()
        if visited is None:
            visited = set(range(len(tiles)))
        self._build_anchor_grid(slide, slide_num, title, subtitle, tiles,
                                visited=visited)
        if notes:
            self._add_speaker_notes(slide, notes)
        self._add_footer(slide)
        return slide

    # ── Public: Pop-up Slides (WHITE panel on dark slide) ────────

    def add_popup_text(self, slide_num, anchor_title, comp_num, comp_title,
                       body="", bullets=None, notes=""):
        """Pop-up: white panel with full-width text + checkmark bullets."""
        slide = self._new_slide()
        self._add_slide_title(slide, anchor_title)
        self._add_layout_badge(slide, slide_num, "Pop-up on anchor")
        self._add_popup_white_panel(slide)
        self._add_popup_header(slide, comp_num, comp_title)
        ct = POPUP_CONTENT_TOP
        if body:
            self._add_text(slide, body, POPUP_CONTENT_LEFT, ct,
                           POPUP_CONTENT_WIDTH, Inches(1.2),
                           size=Pt(16), color=CHARCOAL)
            ct += Inches(1.0)
        if bullets:
            self._add_check_bullets(slide, bullets, POPUP_CONTENT_LEFT, ct,
                                    POPUP_CONTENT_WIDTH, Inches(3.5),
                                    size=Pt(15), text_color=CHARCOAL)
        if notes:
            self._add_speaker_notes(slide, notes)
        self._add_footer(slide)
        return slide

    def add_popup_text_media(self, slide_num, anchor_title, comp_num, comp_title,
                             bullets=None, media_label="", body="", notes=""):
        """Pop-up: white panel with text/bullets left + media placeholder right."""
        slide = self._new_slide()
        self._add_slide_title(slide, anchor_title)
        self._add_layout_badge(slide, slide_num, "Pop-up on anchor")
        self._add_popup_white_panel(slide)
        self._add_popup_header(slide, comp_num, comp_title)
        ct = POPUP_CONTENT_TOP
        lw = Inches(6)
        if body:
            self._add_text(slide, body, POPUP_CONTENT_LEFT, ct,
                           lw, Inches(1), size=Pt(15), color=CHARCOAL)
            ct += Inches(0.8)
        if bullets:
            self._add_check_bullets(slide, bullets, POPUP_CONTENT_LEFT, ct,
                                    lw, Inches(3.5), size=Pt(14),
                                    text_color=CHARCOAL)
        if media_label:
            self._add_media_placeholder(slide, media_label,
                                        Inches(7.5), POPUP_CONTENT_TOP,
                                        Inches(5), Inches(4), on_white=True)
        if notes:
            self._add_speaker_notes(slide, notes)
        self._add_footer(slide)
        return slide

    def add_popup_stepper(self, slide_num, popup_title, comp_num, comp_title,
                          bullets=None, steps=None, extra_sections=None,
                          notes=""):
        """Pop-up: white panel with bullets + stepper/process flow."""
        slide = self._new_slide()
        self._add_slide_title(slide, popup_title)
        self._add_layout_badge(slide, slide_num, "Pop-up on anchor")
        self._add_popup_white_panel(slide)
        self._add_popup_header(slide, comp_num, comp_title)
        ct = POPUP_CONTENT_TOP
        if bullets:
            self._add_check_bullets(slide, bullets, POPUP_CONTENT_LEFT, ct,
                                    Inches(6), Inches(3), size=Pt(13),
                                    text_color=CHARCOAL)
        if steps:
            sx = Inches(7.0)
            sy = POPUP_CONTENT_TOP
            step_w = Inches(1.4)
            for i, (label, caption) in enumerate(steps):
                x = sx + i * (step_w + Inches(0.3))
                box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                                             x, sy, step_w, Inches(0.8))
                box.fill.solid()
                box.fill.fore_color.rgb = COMPONENT_BLUE
                box.line.fill.background()
                self._add_text(slide, label, x, sy, step_w, Inches(0.8),
                               size=Pt(12), color=WHITE, bold=True,
                               align=PP_ALIGN.CENTER)
                if i < len(steps) - 1:
                    arrow = slide.shapes.add_shape(
                        MSO_SHAPE.RIGHT_ARROW,
                        x + step_w + Inches(0.02), sy + Inches(0.25),
                        Inches(0.26), Inches(0.3))
                    arrow.fill.solid()
                    arrow.fill.fore_color.rgb = MED_GRAY
                    arrow.line.fill.background()
            for i, (label, caption) in enumerate(steps):
                x = sx + i * (step_w + Inches(0.3))
                self._add_text(slide, caption, x, sy + Inches(0.9),
                               step_w, Inches(0.6), size=Pt(10),
                               color=DARK_GRAY, align=PP_ALIGN.CENTER)
        if extra_sections:
            ey = Inches(4.8)
            for sec_title, sec_items in extra_sections:
                self._add_section_label(slide, sec_title,
                                        POPUP_CONTENT_LEFT, ey,
                                        color=COMPONENT_BLUE)
                ey += Inches(0.3)
                for item in sec_items:
                    self._add_text(slide, item, POPUP_CONTENT_LEFT + Inches(0.3), ey,
                                   Inches(11), Pt(18), size=Pt(12), color=DARK_GRAY)
                    ey += Inches(0.3)
                ey += Inches(0.15)
        if notes:
            self._add_speaker_notes(slide, notes)
        self._add_footer(slide)
        return slide

    def add_popup_compare(self, slide_num, popup_title, comp_num, comp_title,
                          col_a_header="", col_a_items=None,
                          col_b_header="", col_b_items=None,
                          key_message="", notes=""):
        """Pop-up: white panel with 2-column comparison."""
        slide = self._new_slide()
        self._add_slide_title(slide, popup_title)
        self._add_layout_badge(slide, slide_num, "Pop-up on anchor")
        self._add_popup_white_panel(slide)
        self._add_popup_header(slide, comp_num, comp_title)
        self._add_section_label(slide, "WHAT THIS COMPONENT COVERS",
                                POPUP_CONTENT_LEFT, POPUP_CONTENT_TOP,
                                color=COMPONENT_BLUE)
        col_w = Inches(5.5)
        ax = POPUP_CONTENT_LEFT
        self._add_section_label(slide, col_a_header, ax,
                                POPUP_CONTENT_TOP + Inches(0.5), color=CHARCOAL)
        if col_a_items:
            self._add_bullets(slide, col_a_items,
                              ax + Inches(0.2), POPUP_CONTENT_TOP + Inches(0.9),
                              col_w, Inches(2.5), size=Pt(13),
                              bullet_color=COMPONENT_BLUE, text_color=CHARCOAL)
        bx = Inches(7.0)
        self._add_section_label(slide, col_b_header, bx,
                                POPUP_CONTENT_TOP + Inches(0.5), color=CHARCOAL)
        if col_b_items:
            self._add_bullets(slide, col_b_items,
                              bx + Inches(0.2), POPUP_CONTENT_TOP + Inches(0.9),
                              col_w, Inches(2.5), size=Pt(13),
                              bullet_color=COMPONENT_BLUE, text_color=CHARCOAL)
        if key_message:
            self._add_section_label(slide, "KEY MESSAGE",
                                    POPUP_CONTENT_LEFT, Inches(5.5),
                                    color=COMPONENT_BLUE)
            self._add_text(slide, key_message, POPUP_CONTENT_LEFT, Inches(5.8),
                           POPUP_CONTENT_WIDTH, Inches(0.6),
                           size=Pt(14), color=DARK_GRAY)
        if notes:
            self._add_speaker_notes(slide, notes)
        self._add_footer(slide)
        return slide

    def add_popup_grid(self, slide_num, popup_title, comp_num, comp_title,
                       key_message="", grid_items=None, notes=""):
        """Pop-up: white panel with 2x2 grid.
        grid_items: list of (header, body) tuples."""
        slide = self._new_slide()
        self._add_slide_title(slide, popup_title)
        self._add_layout_badge(slide, slide_num, "Pop-up on anchor")
        self._add_popup_white_panel(slide)
        self._add_popup_header(slide, comp_num, comp_title)
        if key_message:
            self._add_section_label(slide, "KEY MESSAGE",
                                    POPUP_CONTENT_LEFT, POPUP_CONTENT_TOP,
                                    color=COMPONENT_BLUE)
            self._add_text(slide, key_message,
                           POPUP_CONTENT_LEFT, POPUP_CONTENT_TOP + Inches(0.3),
                           POPUP_CONTENT_WIDTH, Inches(0.5),
                           size=Pt(13), color=DARK_GRAY)
        if grid_items:
            grid_w = Inches(5.5)
            grid_h = Inches(1.3)
            gap_x = Inches(0.4)
            gap_y = Inches(0.3)
            start_y = POPUP_CONTENT_TOP + Inches(1.0)
            for i, (header, body) in enumerate(grid_items[:4]):
                col = i % 2
                row = i // 2
                x = POPUP_CONTENT_LEFT + col * (grid_w + gap_x)
                y = start_y + row * (grid_h + gap_y)
                self._add_content_box(slide, x, y, grid_w, grid_h,
                                      fill_color=FAINT_GRAY, border_color=BORDER_LIGHT)
                self._add_section_label(slide, header, x + Inches(0.2),
                                        y + Inches(0.1), width=grid_w,
                                        color=COMPONENT_BLUE)
                self._add_text(slide, body, x + Inches(0.2), y + Inches(0.4),
                               grid_w - Inches(0.4), grid_h - Inches(0.5),
                               size=Pt(13), color=CHARCOAL)
        if notes:
            self._add_speaker_notes(slide, notes)
        self._add_footer(slide)
        return slide

    # ── Legacy alias ─────────────────────────────────────────────

    def add_L12(self, slide_num, title, tiles, notes=""):
        return self.add_anchor(slide_num, title, tiles, notes=notes)

    # ── Public: Layout L13 — Objective / Agenda ──────────────────

    def add_L13(self, slide_num, title, objectives, notes=""):
        slide = self._new_slide()
        self._add_slide_title(slide, title)
        self._add_layout_badge(slide, slide_num, "L13")
        y = Inches(1.8)
        for i, obj in enumerate(objectives):
            circle = slide.shapes.add_shape(MSO_SHAPE.OVAL,
                                            LEFT_MARGIN, y, Inches(0.4), Inches(0.4))
            circle.fill.solid()
            circle.fill.fore_color.rgb = COMPONENT_BLUE
            circle.line.fill.background()
            self._add_text(slide, str(i + 1), LEFT_MARGIN, y,
                           Inches(0.4), Inches(0.4), size=Pt(14),
                           color=WHITE, bold=True, align=PP_ALIGN.CENTER)
            self._add_text(slide, obj, LEFT_MARGIN + Inches(0.6), y,
                           Inches(11), Inches(0.5), size=Pt(16))
            y += Inches(0.7)
        if notes:
            self._add_speaker_notes(slide, notes)
        self._add_footer(slide)
        return slide

    # ── Public: Layout L14 — Summary ─────────────────────────────

    def add_L14(self, slide_num, title, takeaways, cta="Continue", notes=""):
        slide = self._new_slide()
        self._add_slide_title(slide, title)
        self._add_layout_badge(slide, slide_num, "L14")
        self._add_bullets(slide, takeaways, LEFT_MARGIN, Inches(1.8),
                          CONTENT_WIDTH, Inches(4))
        btn = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                                     Inches(10.5), Inches(6.2), Inches(2), Inches(0.5))
        btn.fill.solid()
        btn.fill.fore_color.rgb = COMPONENT_BLUE
        btn.line.fill.background()
        self._add_text(slide, cta, Inches(10.5), Inches(6.2),
                       Inches(2), Inches(0.5), size=Pt(14),
                       color=WHITE, bold=True, align=PP_ALIGN.CENTER)
        if notes:
            self._add_speaker_notes(slide, notes)
        self._add_footer(slide)
        return slide

    # ── Save ─────────────────────────────────────────────────────

    def save(self, path):
        self.prs.save(path)
        print(f"Storyboard saved: {path} ({self.slide_count} slides)")
