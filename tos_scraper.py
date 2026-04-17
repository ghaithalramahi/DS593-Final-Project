"""
ToS Scraper for DS593 Final Project
Scrapes Terms of Service documents from major apps and saves as plain text.
"""

import requests
from bs4 import BeautifulSoup
import time
import os
import json
from datetime import datetime

# ── Config ──────────────────────────────────────────────────────────────────

OUTPUT_DIR = "tos_corpus"
SCRAPE_DATE = datetime.today().strftime("%Y-%m-%d")

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

# ── Target Companies ─────────────────────────────────────────────────────────
# Add or remove as needed. Each entry has:
#   name:         company name (used for filename)
#   tos_url:      Terms of Service URL
#   privacy_url:  Privacy Policy URL (optional but recommended)

COMPANIES = [
    {
        "name": "spotify",
        "tos_url": "https://www.spotify.com/us/legal/end-user-agreement/",
        "privacy_url": "https://www.spotify.com/us/legal/privacy-policy/",
    },
    {
        "name": "instagram",
        "tos_url": "https://help.instagram.com/581066165581870",
        "privacy_url": "https://privacycenter.instagram.com/policy",
    },
    {
        "name": "tiktok",
        "tos_url": "https://www.tiktok.com/legal/page/us/terms-of-service/en",
        "privacy_url": "https://www.tiktok.com/legal/page/us/privacy-policy/en",
    },
    {
        "name": "venmo",
        "tos_url": "https://venmo.com/legal/us-user-agreement/",
        "privacy_url": "https://venmo.com/legal/us-privacy-policy/",
    },
    {
        "name": "airbnb",
        "tos_url": "https://www.airbnb.com/help/article/2908",
        "privacy_url": "https://www.airbnb.com/help/article/2855",
    },
    {
        "name": "uber",
        "tos_url": "https://www.uber.com/legal/en/document/?name=general-terms-of-use&country=united-states&lang=en",
        "privacy_url": "https://www.uber.com/legal/en/document/?name=privacy-notice&country=united-states&lang=en",
    },
    {
        "name": "netflix",
        "tos_url": "https://help.netflix.com/legal/termsofuse",
        "privacy_url": "https://help.netflix.com/legal/privacy",
    },
    {
        "name": "twitter_x",
        "tos_url": "https://twitter.com/en/tos",
        "privacy_url": "https://twitter.com/en/privacy",
    },
    {
        "name": "google",
        "tos_url": "https://policies.google.com/terms",
        "privacy_url": "https://policies.google.com/privacy",
    },
    {
        "name": "facebook",
        "tos_url": "https://www.facebook.com/legal/terms",
        "privacy_url": "https://www.facebook.com/privacy/policy/",
    },
    {
        "name": "amazon",
        "tos_url": "https://www.amazon.com/gp/help/customer/display.html?nodeId=GLSBYFE9MGKKQXXM",
        "privacy_url": "https://www.amazon.com/gp/help/customer/display.html?nodeId=GX7NJQ4ZB8MHFRNJ",
    },
    {
        "name": "paypal",
        "tos_url": "https://www.paypal.com/us/legalhub/useragreement-full",
        "privacy_url": "https://www.paypal.com/us/legalhub/privacy-full",
    },
    {
        "name": "discord",
        "tos_url": "https://discord.com/terms",
        "privacy_url": "https://discord.com/privacy",
    },
    {
        "name": "snapchat",
        "tos_url": "https://snap.com/en-US/terms",
        "privacy_url": "https://snap.com/en-US/privacy/privacy-policy",
    },
    {
        "name": "youtube",
        "tos_url": "https://www.youtube.com/t/terms",
        "privacy_url": "https://policies.google.com/privacy",
    },
    {
        "name": "doordash",
        "tos_url": "https://help.doordash.com/consumers/s/terms-of-service-us",
        "privacy_url": "https://help.doordash.com/consumers/s/privacy-policy",
    },
    {
        "name": "robinhood",
        "tos_url": "https://robinhood.com/us/en/about/legal/",
        "privacy_url": "https://robinhood.com/us/en/about/privacy/",
    },
    {
        "name": "coinbase",
        "tos_url": "https://www.coinbase.com/legal/user_agreement/united_states",
        "privacy_url": "https://www.coinbase.com/legal/privacy",
    },
    {
        "name": "tinder",
        "tos_url": "https://policies.tinder.com/terms/intl/en",
        "privacy_url": "https://policies.tinder.com/privacy/intl/en",
    },
    {
        "name": "linkedin",
        "tos_url": "https://www.linkedin.com/legal/user-agreement",
        "privacy_url": "https://www.linkedin.com/legal/privacy-policy",
    },
]

# ── Scraper ──────────────────────────────────────────────────────────────────

def scrape_page(url: str) -> str:
    """Fetch a URL and return clean plain text."""
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"    ✗ Failed to fetch {url}: {e}")
        return ""

    soup = BeautifulSoup(response.text, "html.parser")

    # Remove boilerplate tags
    for tag in soup(["script", "style", "nav", "footer", "header", "img", "button"]):
        tag.decompose()

    # Extract and clean text
    text = soup.get_text(separator="\n")
    lines = [line.strip() for line in text.splitlines()]
    cleaned = "\n".join(line for line in lines if line)  # drop blank lines

    return cleaned


def save_document(company: str, doc_type: str, text: str):
    """Save scraped text to output directory."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filename = f"{company}_{doc_type}_{SCRAPE_DATE}.txt"
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"    ✓ Saved {filepath} ({len(text):,} chars)")
    return filepath


def scrape_all():
    """Main scraping loop."""
    manifest = []  # track metadata for all scraped docs

    for company in COMPANIES:
        name = company["name"]
        print(f"\n── {name.upper()} ──")

        for doc_type, url in [("tos", company.get("tos_url")), ("privacy", company.get("privacy_url"))]:
            if not url:
                continue

            print(f"  Scraping {doc_type}: {url}")
            text = scrape_page(url)

            if not text or len(text) < 500:
                print(f"    ✗ Too short or empty — may require JS rendering, skip")
                continue

            filepath = save_document(name, doc_type, text)
            manifest.append({
                "company": name,
                "doc_type": doc_type,
                "url": url,
                "filepath": filepath,
                "scrape_date": SCRAPE_DATE,
                "char_count": len(text),
            })

            time.sleep(2)  # polite delay between requests

    # Save manifest
    manifest_path = os.path.join(OUTPUT_DIR, "manifest.json")
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)
    print(f"\n✓ Done. {len(manifest)} documents saved.")
    print(f"✓ Manifest saved to {manifest_path}")

    return manifest


# ── Run ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    scrape_all()
