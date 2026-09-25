"""Рисует картинки профиля: баннер, карточки проектов, стек, активность.

    python gen.py            # всё (нужен gh или GH_TOKEN для активности)
    python gen.py --static   # без обращения к API

Языки и число репозиториев берутся из GitHub API — перезапусти после новых проектов.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import urllib.request
from datetime import date, datetime
from html import escape
from pathlib import Path

LOGIN = "uprtrk"
OUT = Path(__file__).parent / "assets"
OUT.mkdir(exist_ok=True)

BG, BG2 = "#0a0a0a", "#141414"
LINE = "#2a2a2a"
TEXT, MUTED = "#f2f2f2", "#8a8a8a"
C1, C2, C3 = "#ffffff", "#bdbdbd", "#6e6e6e"   # монохром
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,monospace"


def save(name: str, svg: str) -> None:
    (OUT / name).write_text(svg.strip() + "\n", encoding="utf-8")
    print("wrote", name)


# ---------------------------------------------------------------- баннер

def banner() -> None:
    chips = [("flip-tracker", "python"), ("translator-hn", "next.js"),
             ("dvadruga-site", "html/css"), ("fitness-bot", "aiogram")]
    chip_svg = ""
    for i, (name, tag) in enumerate(chips):
        y = 70 + i * 44
        chip_svg += f"""
  <g class="chip" style="animation-delay:{0.4 + i * 0.15}s">
    <rect x="850" y="{y}" width="300" height="32" rx="8" fill="#111111" stroke="{LINE}"/>
    <circle cx="868" cy="{y + 16}" r="4" fill="{C1}"><animate attributeName="opacity" values="1;.3;1" dur="{2 + i * .4}s" repeatCount="indefinite"/></circle>
    <text x="882" y="{y + 21}" font-family="{MONO}" font-size="13" fill="{TEXT}">{name}</text>
    <text x="1136" y="{y + 21}" font-family="{MONO}" font-size="11" fill="{MUTED}" text-anchor="end">{tag}</text>
  </g>"""
    stars = "".join(
        f'<circle cx="{(i * 137) % 1200}" cy="{(i * 71) % 190 + 10}" r="{1 + i % 2 * .6}" fill="#fff" opacity=".35">'
        f'<animate attributeName="opacity" values=".1;.6;.1" dur="{3 + i % 5}s" begin="{i % 7 * .5}s" repeatCount="indefinite"/></circle>'
        for i in range(28))
    save("banner.svg", f"""
<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="300" viewBox="0 0 1200 300">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{BG}"/><stop offset="1" stop-color="#161616"/>
    </linearGradient>
    <linearGradient id="title" x1="0" x2="1">
      <stop offset="0" stop-color="{C1}"/><stop offset=".55" stop-color="{C2}"/><stop offset="1" stop-color="{C3}"/>
    </linearGradient>
    <radialGradient id="glow" cx=".25" cy=".35" r=".6">
      <stop offset="0" stop-color="{C2}" stop-opacity=".28"/><stop offset="1" stop-color="{C2}" stop-opacity="0"/>
    </radialGradient>
    <filter id="grain"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" stitchTiles="stitch"/><feColorMatrix values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 .09 0"/></filter>
    <clipPath id="r"><rect width="1200" height="300" rx="18"/></clipPath>
    <style>
      .fade {{ opacity:0; animation: in .8s ease-out forwards; }}
      .chip {{ opacity:0; animation: slide .6s ease-out forwards; }}
      .type {{ animation: type 2.4s steps(44) .6s both; }}
      .cursor {{ animation: blink 1s step-end infinite; }}
      .wave1 {{ animation: wave 9s linear infinite; }}
      .wave2 {{ animation: wave 14s linear infinite reverse; }}
      @keyframes in {{ from {{ opacity:0; transform: translateY(8px) }} to {{ opacity:1; transform:none }} }}
      @keyframes slide {{ from {{ opacity:0; transform: translateX(20px) }} to {{ opacity:1; transform:none }} }}
      @keyframes type {{ from {{ width:0 }} to {{ width:450px }} }}
      @keyframes blink {{ 50% {{ opacity:0 }} }}
      @keyframes wave {{ from {{ transform: translateX(0) }} to {{ transform: translateX(-600px) }} }}
    </style>
  </defs>
  <g clip-path="url(#r)">
    <rect width="1200" height="300" fill="url(#bg)"/>
    <rect width="1200" height="300" fill="url(#glow)"/>
    {stars}
    <g class="wave2" opacity=".10">
      <path d="M0 262 Q75 248 150 262 T300 262 T450 262 T600 262 T750 262 T900 262 T1050 262 T1200 262 T1350 262 T1500 262 T1650 262 T1800 262 V300 H0Z" fill="{C2}"/>
    </g>
    <g class="wave1" opacity=".16">
      <path d="M0 274 Q75 262 150 274 T300 274 T450 274 T600 274 T750 274 T900 274 T1050 274 T1200 274 T1350 274 T1500 274 T1650 274 T1800 274 V300 H0Z" fill="{C1}"/>
    </g>
    <text class="fade" style="animation-delay:.15s" x="60" y="152" font-family="{SANS}" font-size="76" font-weight="800" fill="url(#title)">uprtrk</text>
    <svg x="64" y="172" width="450" height="30" class="type">
      <text x="0" y="21" font-family="{MONO}" font-size="17" fill="{TEXT}"><tspan fill="{C1}">$</tspan> python · telegram bots · scrapers · websites</text>
    </svg>
    <rect class="cursor" x="516" y="178" width="9" height="20" fill="{C1}"/>
    <text class="fade" style="animation-delay:.3s" x="64" y="232" font-family="{SANS}" font-size="14" fill="{MUTED}">Montenegro · open to freelance</text>
    {chip_svg}
    <rect width="1200" height="300" filter="url(#grain)"/>
  </g>
  <rect x=".5" y=".5" width="1199" height="299" rx="18" fill="none" stroke="{LINE}"/>
</svg>""")


# ---------------------------------------------------------------- карточки

PROJECTS = [
    ("flip", "Flip Tracker", "Deal-finder for reselling electronics",
     ["4.9k listings crawled daily", "212 model rules · 384 tests"],
     ["Python", "Telethon", "Claude API"], "#ffffff", "#3a3a3a"),
    ("translator", "Translator site", "Three-language personal website",
     ["RU · EN · SR", "Editorial design, JSON-LD"],
     ["Next.js 16", "TypeScript", "Tailwind"], "#e0e0e0", "#333333"),
    ("dvadruga", "Dva Druga", "Yacht cleaning in the Bay of Kotor",
     ["Live · 2druga.netlify.app", "8 pages, local SEO"],
     ["HTML", "CSS", "JS"], "#cfcfcf", "#2e2e2e"),
    ("fitness", "FitnessBot", "Workout diary Telegram bot",
     ["Live · @TreningTraker_bot", "Premium via Telegram Stars"],
     ["aiogram 3", "PostgreSQL", "Docker"], "#bdbdbd", "#292929"),
]


def cards() -> None:
    for key, title, sub, facts, tags, accent, deep in PROJECTS:
        tag_svg, x = "", 24
        for t in tags:
            w = 16 + len(t) * 7.4
            tag_svg += (f'<rect x="{x}" y="176" width="{w:.0f}" height="24" rx="6" fill="{accent}" fill-opacity=".12" stroke="{accent}" stroke-opacity=".35"/>'
                        f'<text x="{x + w / 2:.0f}" y="192" font-family="{MONO}" font-size="12" fill="{accent}" text-anchor="middle">{escape(t)}</text>')
            x += w + 8
        facts_svg = "".join(
            f'<text x="24" y="{124 + i * 22}" font-family="{SANS}" font-size="13" fill="{MUTED}">› {escape(f)}</text>'
            for i, f in enumerate(facts))
        save(f"card-{key}.svg", f"""
<svg xmlns="http://www.w3.org/2000/svg" width="440" height="220" viewBox="0 0 440 220">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{deep}" stop-opacity=".55"/><stop offset=".6" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/>
    </linearGradient>
    <linearGradient id="bar" x1="0" x2="1"><stop offset="0" stop-color="{accent}"/><stop offset="1" stop-color="{accent}" stop-opacity="0"/></linearGradient>
    <style>.sh {{ animation: sh 3.5s ease-in-out infinite; }} @keyframes sh {{ 0%,100% {{ opacity:.5 }} 50% {{ opacity:1 }} }}</style>
    <filter id="grain"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" stitchTiles="stitch"/><feColorMatrix values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 .09 0"/></filter>
  </defs>
  <rect x=".5" y=".5" width="439" height="219" rx="14" fill="url(#g)" stroke="{LINE}"/>
  <rect class="sh" x="1" y="216" width="438" height="3" rx="1.5" fill="url(#bar)"/>
  <circle cx="30" cy="30" r="5" fill="{accent}"/>
  <text x="44" y="35" font-family="{MONO}" font-size="12" fill="{MUTED}">github.com/uprtrk</text>
  <text x="24" y="76" font-family="{SANS}" font-size="26" font-weight="700" fill="{TEXT}">{escape(title)}</text>
  <text x="24" y="99" font-family="{SANS}" font-size="14" fill="{accent}">{escape(sub)}</text>
  {facts_svg}
  {tag_svg}
  <rect x="1" y="1" width="438" height="218" rx="14" filter="url(#grain)"/>
</svg>""")


# ---------------------------------------------------------------- стек

STACK = [("Python", "#d0d0d0"), ("aiogram", "#d0d0d0"), ("Telethon", "#d0d0d0"),
         ("SQLAlchemy", "#d0d0d0"), ("PostgreSQL", "#d0d0d0"), ("SQLite", "#d0d0d0"),
         ("Docker", "#d0d0d0"), ("Claude API", "#d0d0d0"), ("TypeScript", "#d0d0d0"),
         ("Next.js", "#d0d0d0"), ("React", "#d0d0d0"), ("Tailwind", "#d0d0d0"),
         ("HTML · CSS", "#d0d0d0"), ("Git", "#d0d0d0")]


def stack() -> None:
    rows, row, width = [], [], 0
    for name, col in STACK:
        w = 34 + len(name) * 8.2
        if width + w > 1100 and row:
            rows.append((row, width)); row, width = [], 0
        row.append((name, col, w)); width += w + 10
    rows.append((row, width))
    body = ""
    for r, (items, total) in enumerate(rows):
        x = (1200 - (total - 10)) / 2
        y = 20 + r * 48
        for i, (name, col, w) in enumerate(items):
            d = (r * 7 + i) * .06
            body += (f'<g class="p" style="animation-delay:{d:.2f}s">'
                     f'<rect x="{x:.0f}" y="{y}" width="{w:.0f}" height="34" rx="17" fill="#111111" stroke="{LINE}"/>'
                     f'<circle cx="{x + 17:.0f}" cy="{y + 17}" r="5" fill="{col}"/>'
                     f'<text x="{x + 28:.0f}" y="{y + 22}" font-family="{MONO}" font-size="14" fill="{TEXT}">{escape(name)}</text></g>')
            x += w + 10
    h = 20 + len(rows) * 48
    save("stack.svg", f"""
<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="{h}" viewBox="0 0 1200 {h}">
  <style>.p {{ opacity:0; animation: p .5s ease-out forwards; }} @keyframes p {{ from {{ opacity:0; transform: translateY(6px) }} to {{ opacity:1; transform:none }} }}</style>
  {body}
</svg>""")


# ---------------------------------------------------------------- активность

def _gql(query: str) -> dict:
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if token:
        req = urllib.request.Request(
            "https://api.github.com/graphql", data=json.dumps({"query": query}).encode(),
            headers={"Authorization": f"bearer {token}", "Content-Type": "application/json"})
        return json.load(urllib.request.urlopen(req))["data"]
    out = subprocess.run(["gh", "api", "graphql", "-f", f"query={query}"],
                         capture_output=True, text=True, encoding="utf-8", check=True)
    return json.loads(out.stdout)["data"]


LANG_COLORS = {"Python": "#f2f2f2", "TypeScript": "#b0b0b0", "HTML": "#7a7a7a",
               "CSS": "#4d4d4d", "JavaScript": "#343434"}


def activity() -> None:
    d = _gql(f"""{{ user(login: "{LOGIN}") {{
      repositories(first: 100, ownerAffiliations: OWNER, isFork: false, privacy: PUBLIC) {{ totalCount
        nodes {{ languages(first: 10) {{ edges {{ size node {{ name }} }} }} }} }} }} }}""")["user"]
    langs: dict[str, int] = {}
    for n in d["repositories"]["nodes"]:
        for e in n["languages"]["edges"]:
            langs[e["node"]["name"]] = langs.get(e["node"]["name"], 0) + e["size"]
    tot = sum(langs.values()) or 1
    top = sorted(langs.items(), key=lambda kv: -kv[1])[:5]

    stats = [(str(d["repositories"]["totalCount"]), "public repositories"),
             ("2", "live products"), ("384", "automated test checks"), ("3", "site languages: ru · en · sr")]
    st = ""
    for i, (v, lab) in enumerate(stats):
        x = 32 + i * 286
        st += (f'<rect x="{x}" y="64" width="270" height="86" rx="10" fill="#111111" stroke="{LINE}"/>'
               f'<text x="{x + 18}" y="108" font-family="{SANS}" font-size="34" font-weight="700" fill="{TEXT}">{v}</text>'
               f'<text x="{x + 18}" y="134" font-family="{MONO}" font-size="12" fill="{MUTED}">{lab}</text>')
    bar, x, legend, lx = "", 32.0, "", 32
    for name, size in top:
        w = 1136 * size / tot
        col = LANG_COLORS.get(name, C2)
        bar += f'<rect x="{x:.1f}" y="200" width="{w:.1f}" height="10" fill="{col}"/>'
        x += w
        legend += (f'<circle cx="{lx + 5}" cy="236" r="5" fill="{col}" stroke="#555"/>'
                   f'<text x="{lx + 16}" y="241" font-family="{MONO}" font-size="12" fill="{TEXT}">{name} <tspan fill="{MUTED}">{100 * size / tot:.0f}%</tspan></text>')
        lx += 36 + len(name) * 8 + 40
    save("activity.svg", f"""
<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="270" viewBox="0 0 1200 270">
  <defs><clipPath id="bar"><rect x="32" y="200" width="1136" height="10" rx="5"/></clipPath></defs>
  <rect x=".5" y=".5" width="1199" height="269" rx="16" fill="{BG}" stroke="{LINE}"/>
  <text x="32" y="42" font-family="{SANS}" font-size="20" font-weight="700" fill="{TEXT}">In numbers</text>
  <text x="156" y="42" font-family="{MONO}" font-size="12" fill="{MUTED}">updated {date.today():%d %b %Y}</text>
  {st}
  <text x="32" y="188" font-family="{MONO}" font-size="12" fill="{MUTED}">languages across public repositories</text>
  <g clip-path="url(#bar)"><rect x="32" y="200" width="1136" height="10" fill="#1a1a1a"/>{bar}</g>
  {legend}
</svg>""")


if __name__ == "__main__":
    banner(); cards(); stack()
    if "--static" not in sys.argv:
        activity()
