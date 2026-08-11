#!/usr/bin/env python3
"""
weekly_update.py  —  Autonomous weekly refresh for the Sports Deal Tracker.

What it does (no human needed):
  1. Asks Claude (with web search) to pull sports investment / M&A deals reported
     in the tracked newsletters over the last ~10 days.
  2. De-duplicates against data/deals.json (by company name) and appends the new,
     fully-enriched deals in the tracker's schema.
  3. Updates data/newsletters.json (pull date + a fresh edition digest).
  4. build.py then regenerates public/index.html (run separately in the workflow).

Requires the env var ANTHROPIC_API_KEY. Model is configurable via TRACKER_MODEL
(default: claude-sonnet-4-5). Safe to re-run: it never removes or overwrites
existing deals, only appends genuinely new ones.
"""
import os, re, json, sys, datetime

DATA = os.path.join(os.path.dirname(__file__), "data")
DEALS_PATH = os.path.join(DATA, "deals.json")
NL_PATH = os.path.join(DATA, "newsletters.json")
MODEL = os.environ.get("TRACKER_MODEL", "claude-sonnet-4-5")

SECTORS = ["Performance & training","Wellness & lifestyle","Data & analytics","Media & content",
           "Fan engagement","Betting & gaming","Commerce & marketplace","IP & rights","Equipment & gear",
           "Venue & events","Business & operations","Participation & access"]
REGIONS = ["North America","Europe","UK","Asia-Pacific","Middle East","Latin America"]

SOURCES = """- Vetted Sports (newsletter.vettedsports.com)
- Front Office Sports / Asset Class (frontofficesports.com)
- Sportico (sportico.com)
- Boardroom (boardroom.tv)
- Regen Sports (regensports.substack.com)
- Huddle Up (huddleup.substack.com)"""

def norm(s): return "".join(c for c in (s or "").lower() if c.isalnum())

def to_round(stage):
    s = (stage or "").lower()
    if "angel" in s: return "Angel Investment"
    if "pre-seed" in s or "pre seed" in s: return "Pre Seed"
    if "seed" in s: return "Seed"
    if "series a" in s: return "Series A"
    if "series b" in s: return "Series B"
    if "series c" in s: return "Series C"
    if any(x in s for x in ["series d","series e","series f"]): return "Series D+"
    if any(x in s for x in ["acquisition","buyout","majority","minority","stake"]): return "Acquisition/Buyout"
    return "Other"

def fund_lookup(funds):
    idx = {}
    for f in funds:
        idx[norm(f["name"])] = f
    def find(name):
        n = norm(name)
        for k, f in idx.items():
            if k and len(k) > 4 and (k in n or n in k):
                return f
        return None
    return find

PROMPT = f"""You maintain a sports-investment deal tracker. Today is {{today}}.
Using web search, find sports investment / funding / M&A deals ANNOUNCED in roughly the last 10 days
(since {{since}}) that are reported in these newsletters/sources:
{SOURCES}

Include every concrete deal where a company / team / league / asset RECEIVED investment or was ACQUIRED
(fundraises, acquisitions, minority or majority stakes, athlete-ownership, PE/VC). Skip pure sponsorships,
endorsements or partnerships that are not investments. Only real, verifiable deals — never invent anything.

Return ONLY a JSON array (no prose, no markdown). Each object MUST have these keys:
  company, lead_investor, investors (array of strings),
  amount (e.g. "$10M" or "Undisclosed"),
  stage (Angel Investment / Pre Seed / Seed / Series A / Series B / Series C / Series D+ / Growth / Acquisition / Minority stake / Buyout),
  date ("Month D, YYYY"),
  region (one of: {", ".join(REGIONS)}),
  sector (choose ONE of: {", ".join(SECTORS)}),
  desc_simple (2-4 sentences, plain-English for a smart 12-year-old — ONLY what the company/asset does; NO investors/funding/founders/metrics),
  founders (name + 1-sentence background, or ""),
  employees (string or ""),
  financials (concrete metrics or ""),
  newsletter (which source it came from)
If nothing new is found, return []."""

def extract_json_array(text):
    # find the last top-level [...] block
    depth = 0; start = None; best = None
    for i, ch in enumerate(text):
        if ch == "[":
            if depth == 0: start = i
            depth += 1
        elif ch == "]":
            depth -= 1
            if depth == 0 and start is not None:
                best = text[start:i+1]
    if not best:
        return []
    return json.loads(best)

def main():
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        print("ERROR: ANTHROPIC_API_KEY not set — skipping research step.", file=sys.stderr)
        sys.exit(1)
    try:
        import anthropic
    except ImportError:
        print("ERROR: `anthropic` not installed. Run: pip install -r requirements.txt", file=sys.stderr)
        sys.exit(1)

    today = datetime.date.today()
    since = today - datetime.timedelta(days=10)
    prompt = PROMPT.format(today=today.strftime("%B %d, %Y"), since=since.strftime("%B %d, %Y"))

    client = anthropic.Anthropic(api_key=key)
    resp = client.messages.create(
        model=MODEL,
        max_tokens=8000,
        tools=[{"type": "web_search_20250305", "name": "web_search", "max_uses": 12}],
        messages=[{"role": "user", "content": prompt}],
    )
    text = "".join(b.text for b in resp.content if getattr(b, "type", "") == "text")
    try:
        found = extract_json_array(text)
    except Exception as e:
        print(f"Could not parse model output ({e}); no changes written.", file=sys.stderr)
        sys.exit(0)

    funds = json.load(open(os.path.join(DATA, "funds.json")))
    deals = json.load(open(DEALS_PATH))
    find_fund = fund_lookup(funds)
    seen = {norm(d["company"]) for d in deals}
    next_id = max(d["id"] for d in deals) + 1

    added = []
    for x in found:
        co = (x.get("company") or "").strip()
        if not co or norm(co) in seen:
            continue
        if (x.get("sector") not in SECTORS) or (x.get("region") not in REGIONS):
            # keep it but coerce to safe defaults rather than dropping
            x["sector"] = x.get("sector") if x.get("sector") in SECTORS else "Business & operations"
            x["region"] = x.get("region") if x.get("region") in REGIONS else "North America"
        seen.add(norm(co))
        lead = x.get("lead_investor") or ""
        f = find_fund(lead) if lead and lead.lower() not in ("undisclosed", "angel investors") else None
        deals.append({
            "id": next_id, "fund_id": f["id"] if f else None,
            "fund_name": lead or (x.get("investors") or ["Investor"])[0],
            "investors": x.get("investors") or ([lead] if lead else []),
            "company": co, "sector": x["sector"], "main_sector": x["sector"],
            "stage": x.get("stage", ""), "round": to_round(x.get("stage")),
            "amount": x.get("amount", ""), "date": x.get("date", ""), "region": x["region"],
            "type_group": f["type_group"] if f else "", "rel": f.get("rel", "") if f else "",
            "desc_simple": x.get("desc_simple", ""), "founders": x.get("founders", ""),
            "employees": x.get("employees", ""), "financials": x.get("financials", ""),
            "summary": x.get("desc_simple", ""), "source_name": x.get("newsletter", "Newsletters"),
            "source_url": "", "enriched": True, "from_newsletter": x.get("newsletter", ""),
        })
        next_id += 1
        added.append(co)

    # refresh fund deal counts
    from collections import Counter
    have = Counter(d["fund_id"] for d in deals if d.get("fund_id") is not None)
    for f in funds:
        f["deal_count"] = have.get(f["id"], 0); f["tracked"] = f["id"] in have

    json.dump(deals, open(DEALS_PATH, "w"), ensure_ascii=False)
    json.dump(funds, open(os.path.join(DATA, "funds.json"), "w"), ensure_ascii=False)

    # update newsletters pull date + a digest edition of what was added
    try:
        nl = json.load(open(NL_PATH))
        nl["pulled"] = today.strftime("%B %d, %Y")
        if added:
            nl.setdefault("editions", []).insert(0, {
                "newsletter": "Weekly auto-pull",
                "date": today.strftime("%B %d, %Y"),
                "title": f"{len(added)} new deal(s) added this week",
                "url": "",
                "deals": added,
            })
        json.dump(nl, open(NL_PATH, "w"), ensure_ascii=False)
    except Exception as e:
        print(f"(newsletters.json not updated: {e})", file=sys.stderr)

    print(f"Weekly update complete. Added {len(added)} new deal(s): {', '.join(added) if added else 'none'}")

if __name__ == "__main__":
    main()
