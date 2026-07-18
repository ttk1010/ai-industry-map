#!/usr/bin/env python3
"""Render data/{world,areas,characters}.yaml into slides/index.html.

Re-run this after editing the yaml data files, adding a character/background
image, or updating a status/version field. Requires PyYAML:
    uv run --with pyyaml python3 scripts/build_slides.py
"""
import html
import pathlib

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
OUT_PATH = ROOT / "slides" / "index.html"

CIRCLED_DIGITS = "①②③④⑤⑥⑦⑧⑨⑩"

STATUS_LABELS = {
    "updated": "Updated",
    "stable": "Stable",
    "watch": "Watch",
}


def load_data():
    world = yaml.safe_load((DATA_DIR / "world.yaml").read_text(encoding="utf-8"))
    areas = yaml.safe_load((DATA_DIR / "areas.yaml").read_text(encoding="utf-8"))
    characters = yaml.safe_load((DATA_DIR / "characters.yaml").read_text(encoding="utf-8"))
    areas.sort(key=lambda a: a["order"])

    by_category = {}
    by_slug = {}
    for c in characters:
        by_category.setdefault(c["category"], []).append(c)
        by_slug[c["slug"]] = c

    return world, areas, characters, by_category, by_slug


def e(text):
    return html.escape(str(text), quote=True)


def badge_icon(entity_or_glyph, color, size_class="", is_image_candidate=None):
    """Render a badge-icon span. Falls back to a colored initial/glyph disc
    until a real character image exists on disk at `image_path`."""
    if is_image_candidate is not None:
        img_path = ROOT / is_image_candidate["image_path"]
        if img_path.exists():
            rel = "../" + is_image_candidate["image_path"]
            return (
                f'<span class="badge-icon {size_class}" '
                f'style="background-image:url(\'{e(rel)}\'); background-color:{e(color)}"></span>'
            )
    return f'<span class="badge-icon {size_class}" style="background:{e(color)}">{e(entity_or_glyph)}</span>'


def bg_attrs(background_path, extra_class=""):
    """Return (class_attr, style_attr) for a page, using a static
    area/world illustration if it has been generated and saved yet."""
    if background_path:
        img_path = ROOT / background_path
        if img_path.exists():
            cls = f"page {extra_class}".strip()
            style = f' style="background-image:url(\'../{e(background_path)}\')"'
            return cls, style, ' data-has-bg="1"'
    return f"page {extra_class}".strip(), "", ""


def grid_cols_style(count, max_cols=6):
    """Fix the tiles grid to exactly `count` columns (single row) instead of
    letting auto-fit wrap to a second row that would overflow the 16:9
    frame. Beyond max_cols, fall back to wrapping (scrollable) rather than
    squeezing cards unreadably thin."""
    if count <= max_cols:
        return f' style="grid-template-columns: repeat({count}, 1fr);"'
    return ""


def render_overview(world, areas):
    tiles = []
    for i, area in enumerate(areas):
        glyph = CIRCLED_DIGITS[i] if i < len(CIRCLED_DIGITS) else str(i + 1)
        tiles.append(f"""
        <button class="tile" data-goto="page-area-{e(area['id'])}">
          {badge_icon(glyph, "#7A6A4F")}
          <h3>{e(area['title'])}</h3>
          <p>{e(area.get('world_name', ''))} — {e(area['subtitle'])}</p>
          <span class="go-label">開く →</span>
        </button>""")

    cls, style, data_has_bg = bg_attrs(world.get("background_path"))
    grid_style = grid_cols_style(len(areas))
    return f"""
    <section class="{cls}" id="page-overview" data-title="全体像" data-parent=""{data_has_bg}{style}>
      <h1 class="title">AI業界地図 — 全体像</h1>
      <p class="lede">俯瞰図。各エリアをクリックすると一覧ページへ移動します。</p>
      <div class="tiles"{grid_style}>{''.join(tiles)}
      </div>
    </section>"""


def render_area_page(area, members, area_index):
    glyph = CIRCLED_DIGITS[area_index] if area_index < len(CIRCLED_DIGITS) else str(area_index + 1)
    cards = []
    for m in members:
        cards.append(f"""
        <button class="pcard" data-goto="page-{e(m['slug'])}">
          <div class="pin-row"><span class="pin {e(m['status'])}"></span><span class="pin-label">{e(STATUS_LABELS.get(m['status'], m['status']))}</span></div>
          {badge_icon(m['name'][0], m['brand_color'], is_image_candidate=m)}
          <h3>{e(m['name'])}</h3>
          <p class="desc">{e(m['org'])} — {e(m['summary'])}</p>
          <span class="go-label">詳細を見る →</span>
        </button>""")

    cls, style, data_has_bg = bg_attrs(area.get("background_path"))
    world_name = area.get("world_name")
    heading = f"{glyph} {e(area['title'])}" + (f" — {e(world_name)}" if world_name else "")
    grid_style = grid_cols_style(len(members))
    return f"""
    <section class="{cls}" id="page-area-{e(area['id'])}" data-title="{e(area['title'])}" data-parent="page-overview"{data_has_bg}{style}>
      <h1 class="title">{heading}</h1>
      <p class="lede">{e(area['lede'])}</p>
      <div class="tiles"{grid_style}>{''.join(cards)}
      </div>
    </section>"""


def render_detail_page(entity, area, by_slug):
    rows = [
        f'<div class="row"><span>バージョン</span><span>{e(entity["version"])}</span></div>',
        f'<div class="row"><span>ステータス</span><span>{e(entity["status_label"])}</span></div>',
    ]
    for note in entity.get("source_notes") or []:
        rows.append(f'<div class="row"><span>出典</span><span>{e(note)}</span></div>')

    related_links = []
    for rel_slug in entity.get("related") or []:
        rel = by_slug.get(rel_slug)
        if rel:
            related_links.append(
                f'<a href="#" data-goto="page-{e(rel_slug)}">→ {e(rel["name"])}と比較する</a>'
            )
    related_links.append(
        f'<a href="#" data-goto="page-area-{e(area["id"])}">→ {e(area["title"])}一覧に戻る</a>'
    )

    # Detail pages reuse their parent area's background (one image per area,
    # not per product) with a stronger scrim applied via the "detail" class.
    cls, style, data_has_bg = bg_attrs(area.get("background_path"), extra_class="detail")
    return f"""
    <section class="{cls}" id="page-{e(entity['slug'])}" data-title="{e(entity['name'])}" data-parent="page-area-{e(area['id'])}"{data_has_bg}{style}>
      <div class="detail-head">
        {badge_icon(entity['name'][0], entity['brand_color'], size_class="", is_image_candidate=entity)}
        <div>
          <h1 class="title">{e(entity['name'])}</h1>
          <span class="meta">{e(entity['org'])} ／ カテゴリ: {e(area['title'])}</span>
        </div>
      </div>
      <p class="lede">{e(entity['summary'])}</p>
      <div class="factbox">{''.join(rows)}
      </div>
      <div class="related">{''.join(related_links)}
      </div>
    </section>"""


def build():
    world, areas, characters, by_category, by_slug = load_data()

    pages_html = [render_overview(world, areas)]
    for i, area in enumerate(areas):
        members = by_category.get(area["id"], [])
        pages_html.append(render_area_page(area, members, i))
        for m in members:
            pages_html.append(render_detail_page(m, area, by_slug))

    doc = f"""<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AI業界地図</title>
<link rel="stylesheet" href="../assets/css/deck.css">
</head>
<body>
<div class="app">
  <nav class="crumbs" id="crumbs"></nav>
  <div class="stage-outer">
    <div class="deck-frame" id="deckFrame">
      {''.join(pages_html)}
    </div>
  </div>
  <div class="bottombar">
    <div class="bottombar-inner">
      <button class="navbtn" id="prevBtn">◀ 前へ</button>
      <span class="page-index" id="pageIndex"></span>
      <button class="navbtn" id="fullscreenBtn">⤢ 全画面</button>
      <button class="navbtn" id="nextBtn">次へ ▶</button>
    </div>
  </div>
</div>
<script src="../assets/js/deck.js"></script>
</body>
</html>
"""
    OUT_PATH.write_text(doc, encoding="utf-8")
    print(f"Wrote {OUT_PATH} ({len(pages_html)} pages)")


if __name__ == "__main__":
    build()
