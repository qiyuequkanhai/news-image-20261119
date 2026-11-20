#!/usr/bin/env python3
"""Draw entry.png for the make.fun news-image-20261119 bounty.

A one-page newspaper front page summing up the world news of
Thursday 19 November 2026, drawn with Pillow. Every headline is a
real event of that day, verified against several news sources
(see README.md for the sources).

The layout is a simple vertical flow: a masthead, a dateline, one
lead story, then two rows of two short stories each, then a footer
line. Blocks are stacked in order, so text can never overlap.
Running the script twice produces byte-identical output.
"""
import os

from PIL import Image, ImageDraw, ImageFont

PAGE_W, PAGE_H = 1024, 1024
MARGIN = 46
TEXT_W = PAGE_W - 2 * MARGIN
GUTTER = 28

PAPER = (251, 248, 241)   # warm off-white
INK = (22, 21, 19)        # near-black
RED = (180, 35, 24)       # accent red for kickers
GREY = (91, 86, 78)       # muted grey for the footer

SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


class Page:
    """A drawing surface with a vertical cursor."""

    def __init__(self):
        self.img = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
        self.draw = ImageDraw.Draw(self.img)
        self.y = 0

    def text(self, x, y, s, fnt, fill=INK):
        self.draw.text((x, y), s, font=fnt, fill=fill)

    def rule(self, weight=2):
        self.draw.line([(MARGIN, self.y), (PAGE_W - MARGIN, self.y)],
                       fill=INK, width=weight)

    def gap(self, n):
        self.y += n

    def wrapped(self, x, s, fnt, width, leading, fill=INK):
        """Draw s wrapped to width; advance the cursor past it."""
        words = s.split()
        line = ""
        for word in words:
            trial = (line + " " + word).strip()
            if self.draw.textlength(trial, font=fnt) <= width:
                line = trial
            else:
                if line:
                    self.text(x, self.y, line, fnt, fill)
                    self.y += leading
                line = word
        if line:
            self.text(x, self.y, line, fnt, fill)
            self.y += leading


def scaled(draw, path, s, top_size, max_w):
    """Biggest font up to top_size that fits s inside max_w."""
    size = top_size
    while size > 10:
        fnt = ImageFont.truetype(path, size)
        if draw.textlength(s, font=fnt) <= max_w:
            return fnt
        size -= 2
    return ImageFont.truetype(path, 10)


def story(page, x, width, kicker, headline, summary,
          head_size=30, body_size=23):
    """One short story: red kicker, bold headline, plain summary."""
    kick = ImageFont.truetype(SANS_BOLD, 24)
    page.text(x, page.y, kicker, kick, RED)
    page.y += 30
    page.wrapped(x, headline, ImageFont.truetype(SANS_BOLD, head_size),
                 width, head_size + 6)
    page.y += 6
    page.wrapped(x, summary, ImageFont.truetype(SANS, body_size),
                 width, body_size + 5)


def build():
    p = Page()
    d = p.draw

    # Masthead.
    p.y = 26
    mast = scaled(d, SERIF_BOLD, "THE WORLD TODAY", 88, TEXT_W)
    title = "THE WORLD TODAY"
    p.text((PAGE_W - d.textlength(title, font=mast)) / 2, p.y, title, mast)
    p.y += 86
    p.rule(4)
    p.y += 8
    p.rule(1)
    p.y += 14

    # Dateline row.
    dl = ImageFont.truetype(SANS_BOLD, 25)
    p.text(MARGIN, p.y, "THURSDAY, 19 NOVEMBER 2026", dl)
    right = "ONE DAY  ·  ONE IMAGE"
    p.text(PAGE_W - MARGIN - d.textlength(right, font=dl), p.y, right, dl,
           RED)
    p.y += 30
    p.rule(1)
    p.y += 12

    # Lead story: Denmark approves the Greenland–US defence pact.
    kick = ImageFont.truetype(SANS_BOLD, 24)
    p.text(MARGIN, p.y, "COPENHAGEN  —  THE ARCTIC", kick, RED)
    p.y += 30
    p.wrapped(MARGIN, "Denmark clears US forces to expand in the Arctic",
              ImageFont.truetype(SANS_BOLD, 48), TEXT_W, 54)
    p.y += 6
    p.wrapped(MARGIN,
              "Parliament votes unanimously to approve a defence pact "
              "with Greenland and the United States, letting American "
              "troops build up in the far north while Denmark keeps "
              "sovereignty.",
              ImageFont.truetype(SANS, 24), TEXT_W, 31)
    p.y += 10
    p.rule(1)
    p.y += 12

    # Two rows of two stories.
    col_w = (TEXT_W - GUTTER) // 2
    x_right = MARGIN + col_w + GUTTER
    for row in (
        (("SPACE",
          "Voyager 1 becomes first craft one light-day from Earth",
          "NASA says the 1977 probe has travelled further from home "
          "than any object ever built."),
         ("GAMES",
          "GTA VI launches worldwide after 13 years",
          "Rockstar's sequel opens to rave reviews as players queue "
          "for the biggest game launch in years.")),
        (("THE GULF  —  ENERGY",
          "Three tankers catch fire after hitting mines near Hormuz",
          "Iran says the ships struck mines east of the strait; the "
          "energy agency warns the crisis threatens global supplies."),
         ("ULAANBAATAR",
          "Mongolia's president quits over railway scandal",
          "Parliament accepts Khurelsukh Ukhnaa's resignation after "
          "claims he profited from a rail project.")),
    ):
        saved_y = p.y
        story(p, MARGIN, col_w, *row[0])
        bottom_left = p.y
        p.y = saved_y
        story(p, x_right, col_w, *row[1])
        p.y = max(bottom_left, p.y) + 10
        p.rule(1)
        p.y += 12

    # Footer: the day's other stories on one line.
    foot_line = ("ALSO:  Anthropic prices record $81.3bn IPO at $83 a "
                 "share  ·  South Korea court overturns ex-PM's "
                 "martial-law sentence  ·  US and Venezuela restore "
                 "military ties")
    foot = scaled(d, SANS, foot_line, 22, TEXT_W)
    p.text((PAGE_W - d.textlength(foot_line, font=foot)) / 2, p.y,
           foot_line, foot, GREY)
    p.y += 30

    print("content bottom y =", p.y)
    assert p.y <= 1000, f"layout overflow: bottom y={p.y}"
    return p.img


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(os.path.dirname(here), "entry.png")
    build().save(out, format="PNG", optimize=True)
    size = os.path.getsize(out)
    print(f"wrote {out} ({size} bytes)")
    assert size <= 1048576, "over 1 MiB!"
