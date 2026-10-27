#!/usr/bin/env python3
"""AI Sentinel public-source monitor. Standard library only. No AI keys or model calls.

The output is a *provisional news-signal index*, never a verified global AI risk score.
Only Green/Amber are automated. Orange/Red require accountable independent human review.
"""
from __future__ import annotations

import datetime as dt
import email.utils
import json
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "watch.json"
TODAY = dt.datetime.now(dt.timezone.utc)
LOOKBACK_DAYS = 14
FEEDS = [
    ("OpenAI newsroom", "https://openai.com/news/rss.xml"),
    ("UK AI Security Institute (Turing feed mirror)",
     "https://raw.githubusercontent.com/alan-turing-institute/ai-rss-feeds/main/feeds/aisi-blog.xml"),
    ("Anthropic research (Turing feed mirror)",
     "https://raw.githubusercontent.com/alan-turing-institute/ai-rss-feeds/main/feeds/anthropic-research.xml"),
    ("Hugging Face technical blog", "https://huggingface.co/blog/feed.xml"),
]
ALLOWED_LINK_HOSTS = {
    "openai.com", "www.openai.com", "aisi.gov.uk", "www.aisi.gov.uk",
    "anthropic.com", "www.anthropic.com", "deepmind.google",
    "github.com", "metr.org", "www.metr.org", "huggingface.co", "www.huggingface.co",
}
AI_CONTEXT = re.compile(r"\b(?:ai|artificial intelligence|agent|model|llm|gpt|claude|alignment|frontier)\b", re.I)
SERIOUS = re.compile(
    r"\b(?:unsanctioned|unauthori[sz]ed|exfiltrat\w*|"
    r"containment breach|security breach|escaped|breakout|"
    r"evad\w* oversight|evad\w* monitor\w*|"
    r"bypass\w* control\w*|self.replicat\w*|loss of control|"
    r"sabotag\w*|covert activit\w*|dangerous capabilit\w*)\b", re.I
)
CONCERN = re.compile(
    r"\b(?:misalign\w*|deceiv\w*|decept\w*|"
    r"cyberattack\w*|incident\w*|oversight failure|"
    r"security failure|control failure|safety breach|model misuse)\b", re.I
)
USER_AGENT = "AI-Sentinel-Observatory/0.6 (+https://github.com/KindaMagic/ai-sentinel-observatory)"


def plain(value: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]*>", " ", value or "")).strip()[:450]


def parse_date(text: str) -> dt.datetime | None:
    if not text:
        return None
    try:
        parsed = email.utils.parsedate_to_datetime(text)
    except (ValueError, TypeError):
        try:
            parsed = dt.datetime.fromisoformat(text.replace("Z", "+00:00"))
        except ValueError:
            return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=dt.timezone.utc)
    return parsed.astimezone(dt.timezone.utc)


def direct(node, tag: str) -> str:
    for child in node:
        if child.tag.rsplit("}", 1)[-1] == tag:
            return "".join(child.itertext()).strip()
    return ""


def feed_items(blob: bytes) -> list[dict]:
    if len(blob) > 4_000_000:
        raise ValueError("Feed too large")
    root = ET.fromstring(blob)
    result = []
    for node in root.iter():
        if node.tag.rsplit("}", 1)[-1] not in ("item", "entry"):
            continue
        title = plain(direct(node, "title"))
        link = direct(node, "link")
        if not link:
            for el in node:
                if el.tag.rsplit("}", 1)[-1] == "link" and el.attrib.get("href"):
                    link = el.attrib["href"]
                    if el.attrib.get("rel", "alternate") == "alternate":
                        break
        desc = plain(direct(node, "description") or direct(node, "summary"))
        date = parse_date(direct(node, "pubDate") or direct(node, "published") or direct(node, "updated"))
        if not title or not date or not link:
            continue
        parsed_url = urlparse(link)
        if parsed_url.scheme != "https" or parsed_url.hostname not in ALLOWED_LINK_HOSTS:
            continue
        if date < TODAY - dt.timedelta(days=LOOKBACK_DAYS) or date > TODAY + dt.timedelta(days=1):
            continue
        result.append({"title": title[:180], "url": link[:600],
                       "publishedAt": date.date().isoformat(), "summary": desc[:260]})
    return result


def source_fetch(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/rss+xml, application/atom+xml, text/xml, */*"})
    with urllib.request.urlopen(request, timeout=18) as response:
        data = response.read(4_000_001)
    if len(data) > 4_000_000:
        raise ValueError("Feed too large")
    return data


def classify(item: dict) -> str | None:
    # Titles and abstracts are unverified claims; these rules are deliberately only signal screening.
    message = (item["title"] + " " + item["summary"])[:700]
    if not AI_CONTEXT.search(message):
        return None
    if SERIOUS.search(message):
        return "serious-keyword"
    if CONCERN.search(message):
        return "watch-keyword"
    return None


def generate() -> dict:
    sources, signals = [], []
    seen = set()
    for name, feed_url in FEEDS:
        try:
            items = feed_items(source_fetch(feed_url))
            if not items:
                raise ValueError("No valid recent entries (may be a quiet or outdated source)")
            for item in items:
                label = classify(item)
                if not label or item["url"] in seen:
                    continue
                seen.add(item["url"])
                signals.append(dict(item, source=name, flag=label))
            sources.append({"name": name, "feed": feed_url, "state": "ok", "itemsInWindow": len(items)})
        except Exception as err:
            sources.append({"name": name, "feed": feed_url, "state": "error",
                            "reason": str(err)[:160]})
    healthy = sum(x["state"] == "ok" for x in sources)
    # Different publications may describe the same underlying incident.
    # No severity above Amber can be inferred from unreviewed headlines/abstracts.
    if healthy < 2:
        level, state = None, "insufficient-sources"
    elif signals:
        level, state = "amber", "provisional"
    else:
        level, state = "green", "provisional"
    signals.sort(key=lambda x: (x["publishedAt"], x["flag"] == "serious-keyword"), reverse=True)
    return {
        "schemaVersion": 1,
        "checkedAt": TODAY.isoformat(timespec="seconds").replace("+00:00", "Z"),
        "lookbackDays": LOOKBACK_DAYS,
        "checkStatus": "ok" if healthy == len(FEEDS) else ("partial" if healthy >= 2 else "failed"),
        "sourcesAvailable": healthy,
        "sourcesExpected": len(FEEDS),
        "riskAssessment": {
            "level": level, "state": state, "reviewStatus": "automated-provisional",
            "formalPublicRating": "unassigned",
            "assessedOn": TODAY.date().isoformat(),
            "method": "conservative keyword screening of recent public publication feeds; not validation of claims or an incident count",
            "status": (f"{len(signals)} relevant publication signal(s) in the last {LOOKBACK_DAYS} days "
                       f"across {healthy}/{len(FEEDS)} available feeds. "
                       "Reports may cover the same incident. This is a provisional publication-screening indicator, not a global danger measurement."),
            "warning": "Green never means safe. Amber means publications merit human checking. Orange and Red require independent documented human review and cannot be selected automatically."
        },
        "sources": sources,
        "signals": signals[:25],
        "limitations": [
            "Publication feeds may be delayed, incomplete, duplicated, or unavailable.",
            "Keyword matches are imperfect, can be wrong, and are not independently verified incidents.",
            "Two publishers discussing the same event are not two independent incidents; publication totals do not count incidents.",
            "No model internals or real-time incident sensors are monitored.",
            "No automatic emergency messages, red warnings, or regulatory submissions."
        ]
    }


def main() -> None:
    data = generate()
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"AI Sentinel: {data['checkStatus']}, {data['sourcesAvailable']} of {len(FEEDS)} feeds, "
          f"{len(data['signals'])} screened publications, provisional source-watch={data['riskAssessment']['level']}")
    # A failed check still writes an explicit unknown status. It must never create a green all-clear.
    if data["checkStatus"] == "failed":
        print("Sources insufficient; public status must show unavailable", file=sys.stderr)


if __name__ == "__main__":
    main()
