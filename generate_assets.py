from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math

root = Path(__file__).resolve().parent / "images"
root.mkdir(parents=True, exist_ok=True)

COLORS = {
    "core": (0, 240, 255),
    "dim": (0, 74, 82),
    "warn": (255, 215, 0),
    "crit": (255, 42, 42),
    "base": (10, 12, 16),
    "panel": (20, 24, 32),
    "text": (232, 244, 248),
    "muted": (107, 122, 141),
}


def load_font(size, bold=False):
    fonts_to_try = [
        r"C:\Windows\Fonts\consola.ttf" if not bold else r"C:\Windows\Fonts\consolab.ttf",
        r"C:\Windows\Fonts\cour.ttf",
        r"C:\Windows\Fonts\lucon.ttf",
    ]
    for font_path in fonts_to_try:
        try:
            return ImageFont.truetype(font_path, size)
        except Exception:
            continue
    return ImageFont.load_default()


def draw_glow(draw, img, xy, radius, color, glow_intensity=15):
    glow_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_layer)
    for i in range(glow_intensity, 0, -1):
        alpha = int(180 * (i / glow_intensity) * 0.15)
        r = radius + (i * 3)
        glow_draw.ellipse([xy[0]-r, xy[1]-r, xy[0]+r, xy[1]+r], fill=color + (alpha,))
    glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(3))
    img.paste(glow_layer, (0, 0), glow_layer)
    draw.ellipse([xy[0]-radius, xy[1]-radius, xy[0]+radius, xy[1]+radius], fill=color)


def draw_hexagon(draw, cx, cy, r, fill=None, outline=None, width=1):
    points = [
        (
            cx + r * math.cos(math.pi / 180 * (60 * i)),
            cy + r * math.sin(math.pi / 180 * (60 * i)),
        )
        for i in range(6)
    ]
    draw.polygon(points, fill=fill, outline=outline, width=width)


def draw_rivet(draw, x, y, r=3):
    draw.ellipse([x-r, y-r, x+r, y+r], fill=COLORS["muted"], outline=COLORS["base"], width=1)
    draw.line([x-r+1, y, x+r-1, y], fill=COLORS["base"], width=1)


def draw_segmented_bar(draw, x, y, w, h, segments, active_color, active_segments):
    seg_w = (w - (segments - 1) * 4) / segments
    for i in range(segments):
        seg_x = x + i * (seg_w + 4)
        color = active_color if i < active_segments else COLORS["dim"]
        draw.rectangle([seg_x, y, seg_x + seg_w, y + h], fill=color, outline=COLORS["base"], width=1)


def draw_bolt(draw, cx, cy, s=1.0, fill=None, outline=None, width=2):
    pts = [
        (cx+10*s, cy-70*s), (cx-30*s, cy+8*s), (cx-8*s, cy+8*s),
        (cx-10*s, cy+70*s), (cx+30*s, cy-8*s), (cx+8*s, cy-8*s),
    ]
    draw.polygon(pts, fill=fill, outline=outline, width=width)


def draw_icon(draw, kind, cx, cy, color, s=1.0):
    w = max(2, int(4*s))
    if kind == "bolt":
        draw_bolt(draw, cx, cy, s, fill=color)
    elif kind == "drop":
        draw.polygon([(cx, cy-60*s), (cx-36*s, cy+10*s), (cx+36*s, cy+10*s)], fill=color)
        draw.ellipse([cx-36*s, cy-8*s, cx+36*s, cy+52*s], fill=color)
    elif kind == "snow":
        for ang in (0, 60, 120):
            r = math.radians(ang)
            dx, dy = 55*s*math.cos(r), 55*s*math.sin(r)
            draw.line([cx-dx, cy-dy, cx+dx, cy+dy], fill=color, width=w)
        draw.ellipse([cx-8*s, cy-8*s, cx+8*s, cy+8*s], fill=color)
    elif kind == "cam":
        draw.rectangle([cx-55*s, cy-28*s, cx+20*s, cy+24*s], outline=color, width=w)
        draw.polygon([(cx+24*s, cy-12*s), (cx+55*s, cy-28*s), (cx+55*s, cy+16*s), (cx+24*s, cy+8*s)], fill=color)
        draw.ellipse([cx-32*s, cy-10*s, cx-4*s, cy+12*s], outline=color, width=max(2, int(3*s)))
    elif kind == "gauge":
        draw.ellipse([cx-50*s, cy-50*s, cx+50*s, cy+50*s], outline=color, width=w)
        draw.line([cx, cy, cx+28*s, cy-28*s], fill=color, width=w)
        draw.ellipse([cx-7*s, cy-7*s, cx+7*s, cy+7*s], fill=color)
        for ang in (200, 245, 290, 335):
            r = math.radians(ang)
            draw.line([cx+40*s*math.cos(r), cy+40*s*math.sin(r), cx+50*s*math.cos(r), cy+50*s*math.sin(r)], fill=color, width=3)
    elif kind == "hammer":
        draw.rectangle([cx-42*s, cy-48*s, cx+8*s, cy-18*s], fill=color)
        draw.line([cx-16*s, cy-18*s, cx+34*s, cy+52*s], fill=color, width=max(3, int(8*s)))


def make_hero_cf(path):
    img = Image.new("RGB", (1200, 900), COLORS["base"])
    draw = ImageDraw.Draw(img, "RGBA")
    for x in range(0, 1200, 40):
        draw.line([(x, 0), (x, 900)], fill=(15, 18, 24), width=1)
    for y in range(0, 900, 40):
        draw.line([(0, y), (1200, y)], fill=(15, 18, 24), width=1)

    px1, py1, px2, py2 = 100, 100, 1100, 800
    draw.rectangle([px1, py1, px2, py2], fill=COLORS["panel"], outline=COLORS["dim"], width=2)
    draw.rectangle([px1, py1, px2, py1+40], fill=(15, 18, 24))
    draw.line([(px1, py1+40), (px2, py1+40)], fill=COLORS["core"], width=1)
    for rx, ry in [(px1+15, py1+15), (px2-15, py1+15), (px1+15, py2-15), (px2-15, py2-15)]:
        draw_rivet(draw, rx, ry)

    f_title, f_huge, f_small = load_font(28, True), load_font(80, True), load_font(18)
    draw.text((px1+20, py1+10), "MODULE: APP-E-PANEL-01 // STATUS: ENERGIZADO", fill=COLORS["core"], font=f_title)
    draw.text((150, 190), "APP E", fill=COLORS["text"], font=f_huge)
    draw.text((150, 285), "SERVICIOS", fill=COLORS["text"], font=f_huge)
    draw.text((150, 395), "ELECTRICISTA & HANDYMAN // MÉRIDA", fill=COLORS["warn"], font=f_title)

    cx, cy = 850, 420
    draw.ellipse([cx-150, cy-150, cx+150, cy+150], outline=COLORS["dim"], width=2)
    draw.ellipse([cx-120, cy-120, cx+120, cy+120], outline=COLORS["muted"], width=1)
    draw_glow(draw, img, (cx, cy), 70, COLORS["core"], glow_intensity=20)
    draw_hexagon(draw, cx, cy, 95, outline=COLORS["text"], width=2)
    draw_bolt(draw, cx, cy, 1.1, fill=COLORS["warn"])

    draw.text((150, 550), "VOLTAJE: 127V / 220V // 60Hz", fill=COLORS["text"], font=f_small)
    draw_segmented_bar(draw, 150, 580, 400, 20, 15, COLORS["warn"], 9)
    draw.text((150, 620), "CARGA: 20A // NORMA NOM-001-SEDE", fill=COLORS["text"], font=f_small)
    draw_segmented_bar(draw, 150, 650, 400, 20, 15, COLORS["core"], 5)

    for i in range(6):
        x, y = 150 + i * 70, 705
        on = i != 4
        draw.rectangle([x, y, x + 50, y + 65], fill=(15, 18, 24), outline=COLORS["dim"], width=2)
        lever = COLORS["warn"] if on else COLORS["crit"]
        draw.rectangle([x+15, y+8 if on else y+35, x+35, y+30 if on else y+57], fill=lever)

    img.save(path, quality=95)


def make_logo_cf(path):
    size = 400
    img = Image.new("RGB", (size, size), COLORS["base"])
    draw = ImageDraw.Draw(img, "RGBA")
    cx, cy = size // 2, size // 2
    draw_hexagon(draw, cx, cy, 180, fill=COLORS["panel"], outline=COLORS["dim"], width=3)
    for i in range(6):
        a = math.pi / 180 * (60 * i)
        draw_rivet(draw, cx + 160 * math.cos(a), cy + 160 * math.sin(a), r=4)

    glow_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw_bolt(ImageDraw.Draw(glow_layer), cx, cy, 1.2, fill=COLORS["core"] + (70,))
    glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(12))
    img.paste(glow_layer, (0, 0), glow_layer)
    draw_bolt(draw, cx, cy, 1.2, fill=COLORS["warn"])
    draw.rectangle([cx-45, cy+130, cx+45, cy+140], fill=COLORS["base"])
    draw_glow(draw, img, (cx, cy+135), 4, COLORS["core"], glow_intensity=8)
    img.save(path, quality=95)


def make_detail_cf(path, title, metric, active_segs, icon, accent):
    img = Image.new("RGB", (800, 800), COLORS["base"])
    draw = ImageDraw.Draw(img, "RGBA")
    draw.rectangle([50, 50, 750, 750], fill=COLORS["panel"], outline=COLORS["dim"], width=2)
    draw.rectangle([50, 50, 750, 100], fill=(15, 18, 24))
    draw.line([(50, 100), (750, 100)], fill=COLORS["core"], width=1)
    for rx, ry in [(65, 65), (735, 65), (65, 735), (735, 735)]:
        draw_rivet(draw, rx, ry)

    draw.text((70, 65), f"SUBSYSTEM: {title.upper()}", fill=COLORS["core"], font=load_font(24, True))

    sx, sy, sw, sh = 100, 160, 600, 360
    draw.rectangle([sx, sy, sx+sw, sy+sh], outline=COLORS["dim"], width=1)
    for c in range(1, 12):
        draw.line([(sx + c * 50, sy), (sx + c * 50, sy+sh)], fill=(15, 18, 24), width=1)
    for r in range(1, 6):
        draw.line([(sx, sy + r * 60), (sx+sw, sy + r * 60)], fill=(15, 18, 24), width=1)

    glow_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw_icon(ImageDraw.Draw(glow_layer), icon, 400, 340, accent + (70,), s=1.8)
    glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(18))
    img.paste(glow_layer, (0, 0), glow_layer)
    draw_icon(draw, icon, 400, 340, accent, s=1.8)

    draw.line([(50, 550), (750, 550)], fill=COLORS["dim"], width=1)
    draw.text((100, 600), "OUTPUT METRIC:", fill=COLORS["muted"], font=load_font(18))
    draw.text((100, 625), metric, fill=COLORS["text"], font=load_font(40, True))
    draw.text((400, 600), "CAPACITY:", fill=COLORS["muted"], font=load_font(18))
    draw_segmented_bar(draw, 400, 630, 300, 15, 10, accent, active_segs)
    img.save(path, quality=95)


make_hero_cf(root / "hero-panel.jpg")
make_logo_cf(root / "logo-appe.jpg")
make_detail_cf(root / "svc-electricidad.jpg", "Electricidad", "127/220V", 9, "bolt", COLORS["warn"])
make_detail_cf(root / "svc-plomeria.jpg", "Plomería", "60 PSI", 6, "drop", COLORS["core"])
make_detail_cf(root / "svc-climas.jpg", "Climas", "16°C", 7, "snow", COLORS["core"])
make_detail_cf(root / "svc-camaras.jpg", "CCTV", "1080P", 8, "cam", COLORS["warn"])
make_detail_cf(root / "svc-presurizacion.jpg", "Presurización", "40 PSI", 5, "gauge", COLORS["core"])
make_detail_cf(root / "svc-handyman.jpg", "Handyman", "24/7", 10, "hammer", COLORS["crit"])

print("Cherenkov Forge v1.1 — Alta Tensión:")
for path in sorted(root.iterdir()):
    print(f"{path.name} ({path.stat().st_size // 1024} KB)")
