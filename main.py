"""Render the 27 November 2026 world-news front page as one PNG.

Standard library + Pillow only. No network, no clock, no random numbers.
Every pixel is derived from the constants and story copy below, so two runs
produce byte-identical output.
"""

import hashlib
import os

from PIL import Image, ImageDraw, ImageFont

WIDTH = 1024
HEIGHT = 1024
PAPER = "#F8F5EF"
INK = "#111111"
CRIMSON = "#A51F2B"
GRAY = "#77736E"
NAVY = "#1B2A4A"
WHITE = "#FFFFFF"
FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF = "DejaVuSerif.ttf"
SERIF_BOLD = "DejaVuSerif-Bold.ttf"
SANS = "DejaVuSans.ttf"
SANS_BOLD = "DejaVuSans-Bold.ttf"

EDITION = {
    "masthead": "WORLD DISPATCH",
    "date": "FRIDAY, 27 NOVEMBER 2026",
    "tagline": "GLOBAL EDITION  -  ELEVEN STORIES IN ONE PAGE",
    "sources": "Sources: Reuters, AP, BBC, AFP, Financial Times, Bloomberg, ONS",
    "stamp": "27 NOVEMBER 2026  -  WORLD SUMMARY",
}

LEAD = {
    "kicker": "LEAD STORY  /  GLOBAL TRADE",
    "headline": "New 25% Tariff Plan Roils Global Markets",
    "body": (
        "A proposed 25% blanket duty on major trading partners rattled global "
        "equities on Friday and drew swift retaliation warnings from Ottawa, "
        "Mexico City and Beijing as analysts flagged higher consumer costs."
    ),
    "meta": "Markets and Policy  -  Trade Flows Under Pressure",
}

STAT = {
    "eyebrow": "PROPOSED U.S. IMPORT DUTY",
    "value": "25%",
    "notes": ["Blanket rate on key imports;", "$1.4T annual trade exposed"],
    "pill": "UP 21.6 PTS VS 2024",
    "bars": [("'23", 2.5), ("'24", 3.4), ("'25", 8.0), ("'26*", 25.0)],
}

FEATURES = [
    {
        "kicker": "MIDDLE EAST  /  SECURITY",
        "headline": "Drone Strike Rattles Kuwait Oil Corridor",
        "body": (
            "Air defenses intercepted incoming drones near southern energy "
            "facilities, lifting crude futures as Gulf patrols tightened."
        ),
        "art": "drone",
    },
    {
        "kicker": "ASIA-PACIFIC  /  ENERGY",
        "headline": "Fire Halts Operations at Bangkok Refinery",
        "body": (
            "Crews contained a blaze at a key processing unit near the Chao "
            "Phraya river as regulators opened a safety investigation."
        ),
        "art": "refinery",
    },
    {
        "kicker": "DIPLOMACY  /  GAZA",
        "headline": "Hague Court Presses on Gaza Aid Access",
        "body": (
            "Judges reviewed urgent filings over winter relief crossings "
            "while truce mediators pushed for a renewed ceasefire pause."
        ),
        "art": "court",
    },
    {
        "kicker": "AMERICAS  /  WEATHER",
        "headline": "Coastal Storm Soaks Macy's Parade Route",
        "body": (
            "Driving rain and 45 mph gusts forced handlers to lower giant "
            "balloons across Manhattan and snarled holiday travel."
        ),
        "art": "storm",
    },
    {
        "kicker": "SPACE  /  TECHNOLOGY",
        "headline": "SpaceX Sets Starship Turnaround Record",
        "body": (
            "The company logged another booster catch in Texas, signaling "
            "a faster cadence ahead of 2027 orbital cargo missions."
        ),
        "art": "rocket",
    },
    {
        "kicker": "SPORT  /  CHESS",
        "headline": "World Chess Title Match Remains Deadlocked",
        "body": (
            "A five-hour endgame duel ended in another draw, keeping both "
            "grandmasters level entering the weekend classical rounds."
        ),
        "art": "chess",
    },
]

BRIEFS = [
    {
        "kicker": "UK  /  MIGRATION",
        "headline": "UK Net Migration Drops 22%",
        "body": (
            "Annual net arrivals eased to 428,000 as tighter student and "
            "work visa rules took hold across Britain."
        ),
    },
    {
        "kicker": "EUROPE  /  ECONOMY",
        "headline": "Eurozone Inflation Edges Higher",
        "body": (
            "Flash figures showed consumer prices ticking up on winter "
            "energy bills ahead of December ECB talks."
        ),
    },
    {
        "kicker": "AFRICA  /  RELIEF",
        "headline": "Sudan Aid Routes Under Strain",
        "body": (
            "UN agencies warned damaged bridges and fighting continue to "
            "slow emergency food convoys into Darfur."
        ),
    },
    {
        "kicker": "CLIMATE  /  POLICY",
        "headline": "Post-COP Climate Finance Stalls",
        "body": (
            "Developing nations pressed wealthy states for clearer grant "
            "timelines after tense global climate talks."
        ),
    },
]


def typeface(filename, pixels):
    """Load one DejaVu face at an exact pixel size."""
    return ImageFont.truetype(os.path.join(FONT_DIR, filename), pixels)


def laid_text(draw, box, text, font, fill, leading=0, tracking=0):
    """Wrap words inside box and return the y coordinate after the last line."""
    x0, y0, x1, _ = box
    words = text.split()
    lines = []
    current = ""
    for word in words:
        trial = (current + " " + word).strip()
        if current and draw.textlength(trial, font=font) > x1 - x0:
            lines.append(current)
            current = word
        else:
            current = trial
    if current:
        lines.append(current)
    step = font.size + leading
    y = y0
    for line in lines:
        if tracking:
            cursor = x0
            for ch in line:
                draw.text((cursor, y), ch, font=font, fill=fill)
                cursor += draw.textlength(ch, font=font) + tracking
        else:
            draw.text((x0, y), line, font=font, fill=fill)
        y += step
    return y


def flat_art(kind):
    """Return an original symbolic illustration drawn from primitives."""
    scale = 4
    side = 76 * scale
    pic = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    pen = ImageDraw.Draw(pic)
    p = lambda v: v * scale

    if kind == "drone":
        pen.polygon([(p(8), p(34)), (p(38), p(27)), (p(68), p(34)),
                     (p(38), p(43))], fill=NAVY)
        pen.line([(p(16), p(31)), (p(5), p(19))], fill=INK, width=p(2))
        pen.line([(p(60), p(31)), (p(71), p(19))], fill=INK, width=p(2))
        pen.ellipse([p(31), p(29), p(45), p(41)], outline=CRIMSON, width=p(2))
        pen.arc([p(22), p(12), p(54), p(44)], 200, 340, fill=GRAY, width=p(2))
        pen.arc([p(14), p(6), p(62), p(54)], 210, 330, fill=GRAY, width=p(2))
    elif kind == "refinery":
        pen.rectangle([p(20), p(20), p(37), p(62)], outline=NAVY, width=p(2))
        pen.rectangle([p(42), p(30), p(60), p(62)], outline=NAVY, width=p(2))
        pen.line([(p(20), p(36)), (p(37), p(36))], fill=NAVY, width=p(2))
        pen.line([(p(42), p(46)), (p(60), p(46))], fill=NAVY, width=p(2))
        pen.polygon([(p(27), p(19)), (p(31), p(7)), (p(35), p(19))], fill=CRIMSON)
        pen.polygon([(p(49), p(29)), (p(53), p(16)), (p(57), p(29))], fill=CRIMSON)
        pen.line([(p(8), p(64)), (p(70), p(64))], fill=INK, width=p(2))
    elif kind == "court":
        pen.line([(p(38), p(10)), (p(38), p(62))], fill=NAVY, width=p(3))
        pen.line([(p(12), p(61)), (p(64), p(61))], fill=NAVY, width=p(3))
        pen.line([(p(14), p(26)), (p(62), p(26))], fill=INK, width=p(2))
        for cx in (14, 62):
            pen.line([(p(cx), p(26)), (p(cx), p(44))], fill=GRAY, width=p(2))
        pen.polygon([(p(8), p(48)), (p(26), p(48)), (p(17), p(31))], outline=CRIMSON, width=p(2))
        pen.polygon([(p(50), p(48)), (p(68), p(48)), (p(59), p(31))], outline=CRIMSON, width=p(2))
    elif kind == "storm":
        pen.ellipse([p(12), p(16), p(44), p(38)], fill=NAVY)
        pen.ellipse([p(32), p(12), p(65), p(40)], fill=NAVY)
        pen.rectangle([p(14), p(30), p(63), p(42)], fill=NAVY)
        for x in (20, 34, 48, 60):
            pen.line([(p(x), p(44)), (p(x - 4), p(58))], fill=GRAY, width=p(2))
        pen.polygon([(p(40), p(38)), (p(31), p(55)), (p(39), p(55)),
                     (p(34), p(69)), (p(51), p(48)), (p(42), p(48))], fill=CRIMSON)
    elif kind == "rocket":
        pen.polygon([(p(38), p(6)), (p(48), p(28)), (p(48), p(55)),
                     (p(28), p(55)), (p(28), p(28))], fill=NAVY)
        pen.rectangle([p(28), p(35), p(48), p(40)], fill=CRIMSON)
        pen.line([(p(20), p(55)), (p(14), p(37))], fill=INK, width=p(3))
        pen.line([(p(56), p(55)), (p(62), p(37))], fill=INK, width=p(3))
        pen.polygon([(p(33), p(56)), (p(43), p(56)), (p(38), p(70))], fill=CRIMSON)
    elif kind == "chess":
        pen.polygon([(p(26), p(62)), (p(30), p(38)), (p(37), p(24)),
                     (p(31), p(13)), (p(43), p(13)), (p(47), p(26)),
                     (p(54), p(39)), (p(50), p(62))], fill=NAVY)
        pen.ellipse([p(28), p(8), p(46), p(20)], outline=CRIMSON, width=p(2))
        for row in range(2):
            for col in range(4):
                if (row + col) % 2 == 0:
                    x, y = p(14 + col * 12), p(64 + row * 6)
                    pen.rectangle([x, y, x + p(12), y + p(6)], fill=GRAY)
    else:
        raise ValueError("unknown illustration: " + kind)

    return pic.resize((76, 76), Image.Resampling.LANCZOS)


def hero_stats(draw, x, y, w, h):
    """Draw the crimson focal card with its bar comparison and trend pill."""
    draw.rectangle([x, y, x + w, y + h], fill=CRIMSON)
    eyebrow = typeface(SANS_BOLD, 13)
    figure = typeface(SANS_BOLD, 58)
    note_font = typeface(SANS, 12)
    pill_font = typeface(SANS_BOLD, 11)
    draw.text((x + 20, y + 14), STAT["eyebrow"], font=eyebrow, fill=PAPER,
              tracking=1)
    draw.text((x + 18, y + 34), STAT["value"], font=figure, fill=WHITE)
    ny = y + 104
    for line in STAT["notes"]:
        draw.text((x + 20, ny), line, font=note_font, fill=PAPER)
        ny += 16

    plot_x = x + 158
    plot_y = y + 48
    plot_w = w - 178
    top = 72
    for idx, (label, amount) in enumerate(STAT["bars"]):
        slot = plot_w // 4
        bx = plot_x + idx * slot
        bh = max(6, int(top * amount / 25.0))
        colour = PAPER if idx == 3 else GRAY
        draw.rectangle([bx, plot_y + top - bh, bx + 20, plot_y + top],
                       fill=colour)
        draw.text((bx + 2, plot_y + top + 5), label, font=note_font,
                  fill=PAPER)

    pill_w = int(draw.textlength(STAT["pill"], font=pill_font)) + 24
    draw.rounded_rectangle([x + 18, y + h - 34, x + 18 + pill_w, y + h - 10],
                           radius=10, fill=PAPER)
    draw.text((x + 30, y + h - 30), STAT["pill"], font=pill_font, fill=CRIMSON)


def feature_block(canvas, draw, story, x, y, w, h, art):
    """One illustrated news item in the middle grid."""
    draw.line([(x, y), (x + w, y)], fill=GRAY, width=1)
    kicker = typeface(SANS_BOLD, 13)
    headline = typeface(SERIF_BOLD, 20)
    body = typeface(SANS, 14)
    draw.text((x, y + 12), story["kicker"], font=kicker, fill=CRIMSON,
              tracking=2)
    next_y = laid_text(draw, (x, y + 36, x + w - 92, y + h),
                       story["headline"], headline, INK, leading=3)
    laid_text(draw, (x, next_y + 6, x + w - 92, y + h - 2),
              story["body"], body, GRAY, leading=4)
    canvas.paste(art, (x + w - 76, y + 40), art)


def brief_block(draw, story, x, y, w):
    """One compact text-led item in the ALSO TODAY strip."""
    kicker = typeface(SANS_BOLD, 11)
    headline = typeface(SERIF_BOLD, 16)
    body = typeface(SANS, 12)
    draw.text((x, y), story["kicker"], font=kicker, fill=NAVY, tracking=1)
    next_y = laid_text(draw, (x, y + 20, x + w, y + 80),
                       story["headline"], headline, INK, leading=2)
    laid_text(draw, (x, next_y + 4, x + w, y + 120),
              story["body"], body, GRAY, leading=3)


def render(destination):
    """Draw the whole page and write entry.png into destination."""
    os.makedirs(destination, exist_ok=True)
    paper = Image.new("RGB", (WIDTH, HEIGHT), PAPER)
    draw = ImageDraw.Draw(paper, "RGB")

    draw.rectangle([14, 14, WIDTH - 15, HEIGHT - 15], outline=GRAY, width=1)
    draw.line([(40, 32), (984, 32)], fill=INK, width=3)
    draw.line([(40, 37), (984, 37)], fill=INK, width=1)

    mast = typeface(SERIF_BOLD, 62)
    date_font = typeface(SANS_BOLD, 15)
    tag_font = typeface(SANS, 12)
    draw.text((40, 48), EDITION["masthead"], font=mast, fill=INK)
    draw.line([(40, 120), (984, 120)], fill=CRIMSON, width=2)
    draw.text((40, 129), EDITION["date"], font=date_font, fill=CRIMSON,
              tracking=2)
    draw.text((40, 150), EDITION["tagline"], font=tag_font, fill=GRAY,
              tracking=1)

    lead_font = typeface(SERIF_BOLD, 39)
    lead_body = typeface(SANS, 13)
    meta_font = typeface(SANS_BOLD, 11)
    draw.line([(40, 180), (984, 180)], fill=INK, width=1)
    draw.text((40, 192), LEAD["kicker"], font=meta_font, fill=CRIMSON,
              tracking=2)
    next_y = laid_text(draw, (40, 220, 640, 306), LEAD["headline"],
                       lead_font, INK, leading=2)
    next_y = laid_text(draw, (40, next_y + 4, 640, 358), LEAD["body"],
                       lead_body, GRAY, leading=3)
    draw.text((40, 359), LEAD["meta"], font=meta_font, fill=GRAY)
    hero_stats(draw, 664, 192, 320, 154)

    draw.line([(40, 368), (984, 368)], fill=INK, width=2)
    cell_w = 472
    cell_h = 132
    for index, item in enumerate(FEATURES):
        col, row = index % 2, index // 2
        cx = 40 + col * (cell_w + 4)
        cy = 376 + row * cell_h
        feature_block(paper, draw, item, cx, cy, cell_w, cell_h,
                      flat_art(item["art"]))
        if col == 0:
            draw.line([(516, cy), (516, cy + cell_h - 8)], fill=GRAY, width=1)

    strip_top = 782
    draw.line([(40, strip_top), (984, strip_top)], fill=INK, width=2)
    strip_label = typeface(SANS_BOLD, 13)
    draw.text((40, strip_top + 10), "ALSO TODAY", font=strip_label,
              fill=CRIMSON, tracking=2)
    draw.line([(40, strip_top + 32), (984, strip_top + 32)],
              fill=GRAY, width=1)
    brief_w = 236
    for index, item in enumerate(BRIEFS):
        brief_block(draw, item, 40 + index * brief_w, strip_top + 42,
                    brief_w - 12)

    draw.line([(40, 954), (984, 954)], fill=INK, width=1)
    source_font = typeface(SANS, 11)
    draw.text((40, 966), EDITION["sources"], font=source_font, fill=GRAY)
    stamp_w = draw.textlength(EDITION["stamp"], font=source_font)
    draw.text((984 - stamp_w, 966), EDITION["stamp"], font=source_font,
              fill=GRAY)

    target = os.path.join(destination, "entry.png")
    paper.save(target, format="PNG", optimize=True)
    return target


if __name__ == "__main__":
    folder = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    path = render(folder)
    image = Image.open(path)
    with open(path, "rb") as handle:
        digest = hashlib.sha256(handle.read()).hexdigest()
    print("wrote", path, image.size, digest)
