"""
Weekly Brand vs Non-Brand report: cost per campaign plus conversions and
conversion value per conversion action, both by conversion time and by click time.

Answers "is our scaling only profitable because of brand conversions?" by
splitting every week into campaign groups (Brand, NB High Intent, NB Competitor,
NB Other) and every conversion into its action (e.g. Core / Evolve / Ultimate lead,
soft conversions).

Output is a long-format CSV:
    week_start, campaign_id, campaign, campaign_group, conversion_action,
    cost, clicks, impressions,
    conv_by_conv_time, value_by_conv_time, conv_by_click_time, value_by_click_time

Cost rows have an empty conversion_action. Conversion rows have cost = 0.

Usage:
    python conversion_time_report.py                      # last 12 full weeks
    python conversion_time_report.py --weeks 8
    python conversion_time_report.py --start-date 2026-07-13 --end-date 2026-10-04
    python conversion_time_report.py --output report.csv --brand-pattern "brand|\\bBR\\b"
"""

import argparse
import csv
import re
import sys
from collections import defaultdict
from datetime import date, timedelta

from client import get_client, get_customer_id


def default_range(weeks: int) -> tuple[str, str]:
    """Last `weeks` full Monday-Sunday weeks, ending last Sunday."""
    today = date.today()
    last_sunday = today - timedelta(days=today.weekday() + 1)
    start = last_sunday - timedelta(weeks=weeks) + timedelta(days=1)
    return start.isoformat(), last_sunday.isoformat()


NON_BRAND_RE = re.compile(r"\bNB\b|non[- ]?brand", re.IGNORECASE)


def classify(name: str, brand_re: re.Pattern) -> str:
    # Check non-brand markers first so "Non-Brand ..." never matches the brand pattern.
    if not NON_BRAND_RE.search(name) and brand_re.search(name):
        return "Brand"
    lowered = name.lower()
    if "competitor" in lowered or "lanserhof" in lowered:
        return "NB Competitor"
    if "high intent" in lowered:
        return "NB High Intent"
    return "NB Other"


def run(args):
    start, end = (args.start_date, args.end_date) if args.start_date and args.end_date else default_range(args.weeks)
    brand_re = re.compile(args.brand_pattern, re.IGNORECASE)

    client = get_client()
    customer_id = get_customer_id()
    ga_service = client.get_service("GoogleAdsService")
    where = f"segments.date BETWEEN '{start}' AND '{end}'"

    # Cost metrics are incompatible with segments.conversion_action, so run two queries.
    cost_query = f"""
        SELECT segments.week, campaign.id, campaign.name,
               metrics.cost_micros, metrics.clicks, metrics.impressions
        FROM campaign
        WHERE {where}
    """
    conv_query = f"""
        SELECT segments.week, campaign.id, campaign.name,
               segments.conversion_action_name,
               metrics.conversions, metrics.conversions_value,
               metrics.conversions_by_conversion_date,
               metrics.conversions_value_by_conversion_date
        FROM campaign
        WHERE {where}
    """

    rows = []
    for row in ga_service.search(customer_id=customer_id, query=cost_query):
        m = row.metrics
        if not (m.cost_micros or m.clicks or m.impressions):
            continue
        rows.append({
            "week_start": row.segments.week,
            "campaign_id": row.campaign.id,
            "campaign": row.campaign.name,
            "campaign_group": classify(row.campaign.name, brand_re),
            "conversion_action": "",
            "cost": round(m.cost_micros / 1_000_000, 2),
            "clicks": m.clicks,
            "impressions": m.impressions,
            "conv_by_conv_time": 0, "value_by_conv_time": 0,
            "conv_by_click_time": 0, "value_by_click_time": 0,
        })

    for row in ga_service.search(customer_id=customer_id, query=conv_query):
        m = row.metrics
        if not (m.conversions or m.conversions_by_conversion_date):
            continue
        rows.append({
            "week_start": row.segments.week,
            "campaign_id": row.campaign.id,
            "campaign": row.campaign.name,
            "campaign_group": classify(row.campaign.name, brand_re),
            "conversion_action": row.segments.conversion_action_name,
            "cost": 0, "clicks": 0, "impressions": 0,
            "conv_by_conv_time": round(m.conversions_by_conversion_date, 2),
            "value_by_conv_time": round(m.conversions_value_by_conversion_date, 2),
            "conv_by_click_time": round(m.conversions, 2),
            "value_by_click_time": round(m.conversions_value, 2),
        })

    if not rows:
        print("No data found for the specified range.")
        return

    rows.sort(key=lambda r: (r["week_start"], r["campaign_group"], r["campaign"], r["conversion_action"]))
    with open(args.output, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    # Console summary: Brand vs Non-Brand by conversion time.
    totals = defaultdict(lambda: {"cost": 0.0, "value": 0.0})
    for r in rows:
        key = "Brand" if r["campaign_group"] == "Brand" else "Non-Brand"
        totals[key]["cost"] += r["cost"]
        totals[key]["value"] += r["value_by_conv_time"]

    print(f"\nBrand vs Non-Brand ({start} to {end}), value by conversion time")
    for key in ("Brand", "Non-Brand"):
        t = totals[key]
        roas = t["value"] / t["cost"] if t["cost"] else 0
        print(f"  {key:<10} cost {t['cost']:>10,.2f} | value {t['value']:>11,.2f} | ROAS {roas:.2f}x")
    print(f"\nWrote {len(rows)} rows to {args.output}")
    print("Load the CSV into the Brand vs Non-Brand dashboard to see the weekly breakdown.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Weekly Brand vs Non-Brand conversion report")
    parser.add_argument("--weeks", type=int, default=12, help="Number of full weeks (default 12)")
    parser.add_argument("--start-date", help="Custom start date (YYYY-MM-DD)")
    parser.add_argument("--end-date", help="Custom end date (YYYY-MM-DD)")
    parser.add_argument("--brand-pattern", default=r"brand|\bBR\b",
                        help="Regex that marks a campaign as Brand (case-insensitive)")
    parser.add_argument("--output", default="conversion_time_report.csv", help="CSV output path")
    args = parser.parse_args()
    if bool(args.start_date) != bool(args.end_date):
        sys.exit("Pass both --start-date and --end-date, or neither.")
    run(args)
