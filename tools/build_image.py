#!/usr/bin/env python3
"""Render a one-page newspaper front page for 19 November 2026.

Reads nothing from the network and writes a single deterministic PNG:
entry.png, 1024x1024, in the repository root next to this script's folder.
Run:  python3 tools/build_image.py
"""

from PIL import Image, ImageDraw, ImageFont

PAGE = 1024
MARGIN = 38
INK = (24, 24, 22)
PAPER = (247, 243, 234)
RULE = (120, 110, 96)
ACCENT = (142, 28, 22)
GREY = (96, 92, 84)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
SERIF = FONT_DIR + "DejaVuSerif.ttf"
SERIF_BOLD = FONT_DIR + "DejaVuSerif-Bold.ttf"
SANS = FONT_DIR + "DejaVuSans.ttf"
SANS_BOLD = FONT_DIR + "DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(text, face, width, draw):
    """Greedy word wrap: returns lines that fit inside `width` pixels."""
    lines = []
    for chunk in text.split("\n"):
        words = chunk.split()
        if not words:
            lines.append("")
            continue
        line = words[0]
        for word in words[1:]:
            trial = line + " " + word
            if draw.textlength(trial, font=face) <= width:
                line = trial
            else:
                lines.append(line)
                line = word
        lines.append(line)
    return lines


def draw_wrapped(draw, x, y, text, face, width, leading, fill=INK):
    """Draw wrapped text starting at (x, y); returns the y below the block."""
    for line in wrap(text, face, width, draw):
        draw.text((x, y), line, font=face, fill=fill)
        y += leading
    return y

# --- The day's stories, each checked against several news sources. ---
LEAD_HEADLINE = "Denmark votes 109-0 to back US-Greenland defence pact"
LEAD_DECK = (
    "Parliament ratifies the September accord, clearing the way for bigger "
    "US bases in the Arctic and barring non-NATO forces from the island."
)

STORIES = [
    (
        "SPACE",
        "Voyager 1 phones home from a light-day away",
        "NASA confirmed on Thursday that Voyager 1 has crossed one light-day "
        "from Earth - about 16 billion miles - after 49 years in flight. The "
        "probe stopped sending science data on 14 November, but its carrier "
        "signal still reaches the Deep Space Network.",
    ),
    (
        "GAMES",
        "GTA VI takes an estimated $2.36bn on day one",
        "Rockstar's Grand Theft Auto VI launched at midnight on 19 November "
        "for PlayStation 5 and Xbox Series X|S. Tracker Sensor Tower estimates "
        "24.58 million copies sold in the first day, the biggest entertainment "
        "launch on record. Take-Two has not confirmed a figure.",
    ),
    (
        "ENERGY",
        "Iran says five tankers struck mines in Hormuz",
        "Iran's Revolutionary Guard navy said two supertankers carrying more "
        "than four million barrels of crude hit naval mines and caught fire in "
        "the Strait of Hormuz, and three more tankers were hit east of the "
        "strait. The claims could not be independently verified.",
    ),
    (
        "ASIA",
        "Mongolian parliament accepts president's resignation",
        "Lawmakers voted 96-104 to accept President Khurelsukh Ukhnaa's "
        "resignation, the first time a sitting Mongolian president has left "
        "office early. He quit on 17 November denying corruption allegations "
        "and saying he wants to clear his name; an election must follow "
        "within four months.",
    ),
]

BRIEFS = [
    "Pituffik Space Base in north-west Greenland is to expand under the deal.",
    "Voyager 1 is now heading for the star Gliese 445, some 17 light-years away.",
    "GTA VI scored 99 out of 100 on review aggregator Metacritic.",
]


def rule(draw, y, x0=None, x1=None, width=2):
    """A horizontal rule across the page (or between x0 and x1)."""
    draw.line(
        [(x0 if x0 is not None else MARGIN, y), (x1 if x1 is not None else PAGE - MARGIN, y)],
        fill=RULE,
        width=width,
    )


def story_block(draw, x, y, width, kicker, headline, body):
    """One column story: red kicker, bold headline, justified-feel body."""
    kick = font(SANS_BOLD, 15)
    head = font(SERIF_BOLD, 26)
    text = font(SERIF, 16)
    draw.text((x, y), kicker, font=kick, fill=ACCENT)
    y += 24
    y = draw_wrapped(draw, x, y, headline, head, width, 31)
    y += 6
    y = draw_wrapped(draw, x, y, body, text, width, 22)
    return y

def build():
    canvas = Image.new("RGB", (PAGE, PAGE), PAPER)
    draw = ImageDraw.Draw(canvas)
    content_w = PAGE - 2 * MARGIN
    y = 30

    # Masthead.
    title = font(SERIF_BOLD, 66)
    name = "THE WORLD TODAY"
    tw = draw.textlength(name, font=title)
    draw.text(((PAGE - tw) / 2, y), name, font=title, fill=INK)
    y += 82
    rule(draw, y, width=3)
    y += 10

    # Dateline.
    date_face = font(SANS_BOLD, 17)
    dateline = "THURSDAY 19 NOVEMBER 2026  |  WORLD NEWS IN ONE PAGE"
    dw = draw.textlength(dateline, font=date_face)
    draw.text(((PAGE - dw) / 2, y), dateline, font=date_face, fill=GREY)
    y += 30
    rule(draw, y, width=3)
    y += 16

    # Lead story, full width.
    lead_face = font(SERIF_BOLD, 44)
    y = draw_wrapped(draw, MARGIN, y, LEAD_HEADLINE, lead_face, content_w, 50)
    y += 8
    deck_face = font(SERIF, 20)
    y = draw_wrapped(draw, MARGIN, y, LEAD_DECK, deck_face, content_w, 27, fill=GREY)
    y += 14
    rule(draw, y)
    y += 16

    # Two stories per row, two rows.
    gutter = 28
    col_w = (content_w - gutter) // 2
    row_top = y
    bottoms = []
    for i in range(2):
        kicker, headline, body = STORIES[i]
        end = story_block(draw, MARGIN + i * (col_w + gutter), row_top, col_w,
                          kicker, headline, body)
        bottoms.append(end)
    y = max(bottoms) + 14
    rule(draw, y)
    y += 16
    row_top = y
    bottoms = []
    for i in range(2, 4):
        kicker, headline, body = STORIES[i]
        end = story_block(draw, MARGIN + (i - 2) * (col_w + gutter), row_top, col_w,
                          kicker, headline, body)
        bottoms.append(end)
    y = max(bottoms) + 14
    rule(draw, y, width=3)
    y += 12

    # Briefs strip.
    brief_face = font(SANS_BOLD, 15)
    draw.text((MARGIN, y), "IN BRIEF", font=brief_face, fill=ACCENT)
    y += 24
    item_face = font(SERIF, 15)
    for item in BRIEFS:
        y = draw_wrapped(draw, MARGIN + 16, y, item, item_face,
                         content_w - 16, 20)
        draw.text((MARGIN, y - 20), "-", font=item_face, fill=GREY)
    y += 8
    rule(draw, y)
    y += 10

    # Footer.
    foot = font(SANS, 13)
    note = "THE WORLD TODAY  |  19 November 2026  |  Stories verified against multiple sources"
    fw = draw.textlength(note, font=foot)
    draw.text(((PAGE - fw) / 2, y), note, font=foot, fill=GREY)

    return canvas


def main():
    import os

    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(os.path.dirname(here), "entry.png")
    build().save(out, "PNG")
    print("wrote", out)


if __name__ == "__main__":
    main()
