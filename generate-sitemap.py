pythonCopyEditimport feedparserfrom datetime import datetime, timedeltafrom xml.etree.ElementTree import Element, SubElement, tostringimport xml.dom.minidom
# --- Configuration ---RSS_FEED_URL = "https://www.dailydrop.com/pages/rss.xml"SITE_NAME = "Daily Drop"LANGUAGE = "en"# --- Parse RSS feed ---feed = feedparser.parse(RSS_FEED_URL)
two_days_ago = datetime.utcnow() - timedelta(days=2)
recent_entries = [
    entry for entry in feed.entries
    if datetime(*entry.published_parsed[:6]) > two_days_ago
]
# --- Build XML sitemap ---urlset = Element("urlset", {
    "xmlns": "http://www.sitemaps.org/schemas/sitemap/0.9",
    "xmlns:news": "http://www.google.com/schemas/sitemap-news/0.9"})
for entry in recent_entries:
    url = SubElement(urlset, "url")
    SubElement(url, "loc").text = entry.link

    news = SubElement(url, "news:news")
    pub = SubElement(news, "news:publication")
    SubElement(pub, "news:name").text = SITE_NAME
    SubElement(pub, "news:language").text = LANGUAGE
    SubElement(news, "news:publication_date").text = datetime(*entry.published_parsed[:6]).isoformat() + "Z"    SubElement(news, "news:title").text = entry.title
# --- Write to file ---pretty_xml = xml.dom.minidom.parseString(tostring(urlset, 'utf-8')).toprettyxml(indent="  ")with open("news-sitemap.xml", "w", encoding="utf-8") as f:
    f.write(pretty_xml)
