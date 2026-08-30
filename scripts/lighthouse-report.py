#!/usr/bin/env python3
"""Pretty-print Lighthouse JSON reports into a compact scorecard.

Usage: lighthouse-report.py report1.json [report2.json ...]
"""
import json
import sys


def display(audit):
    dv = audit.get("displayValue")
    if isinstance(dv, dict):
        return dv.get("value") or ""
    return dv or ""


def report(path):
    r = json.load(open(path))
    url = r.get("finalDisplayedUrl", path)
    cats = r["categories"]
    a = r["audits"]
    print(f"\n=== {url} ===")
    for key in ("performance", "accessibility", "best-practices", "seo"):
        print(f"  {cats[key]['title']:16} {round(cats[key]['score'] * 100)}")
    for key, label in (
        ("first-contentful-paint", "FCP"),
        ("largest-contentful-paint", "LCP"),
        ("total-blocking-time", "TBT"),
        ("cumulative-layout-shift", "CLS"),
        ("speed-index", "SI"),
    ):
        if key in a:
            print(f"  {label:16} {display(a[key])}")
    fails = []
    for cat in cats.values():
        for ref in cat["auditRefs"]:
            aud = a.get(ref["id"], {})
            s = aud.get("score")
            if (
                s is not None
                and s < 0.9
                and aud.get("scoreDisplayMode") not in ("informative", "notApplicable", "manual")
            ):
                fails.append(f"[{cat['title'][:4]}] {aud['title']}")
    if fails:
        print("  -- замечания (score < 90):")
        for f in fails[:12]:
            print(f"     • {f}")


if __name__ == "__main__":
    for p in sys.argv[1:]:
        report(p)
