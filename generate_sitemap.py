#!/usr/bin/env python3
import json
import os

def generate_sitemap():
    with open('events-data.json', 'r') as f:
        events = json.load(f)
    
    sitemap = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'''
    
    base_urls = [
        ("https://whenisthenext.com/", "2026-04-16", "daily", "1.0"),
        ("https://whenisthenext.com/f1/index.html", "2026-04-16", "weekly", "0.9"),
        ("https://whenisthenext.com/steam/index.html", "2026-04-16", "weekly", "0.9"),
        ("https://whenisthenext.com/apple/index.html", "2026-04-16", "weekly", "0.9"),
        ("https://whenisthenext.com/prime-day/index.html", "2026-04-16", "weekly", "0.9"),
    ]
    
    for url, lastmod, changefreq, priority in base_urls:
        sitemap += f'''
    <url>
        <loc>{url}</loc>
        <lastmod>{lastmod}</lastmod>
        <changefreq>{changefreq}</changefreq>
        <priority>{priority}</priority>
    </url>'''
    
    for event in events:
        slug = event['slug']
        date = event['date']
        url = f"https://whenisthenext.com/events/{slug}/index.html"
        sitemap += f'''
    <url>
        <loc>{url}</loc>
        <lastmod>{date}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.5</priority>
    </url>'''
    
    sitemap += '''
</urlset>'''
    
    with open('sitemap.xml', 'w') as f:
        f.write(sitemap)
    
    print(f"Generated sitemap.xml with {len(events) + len(base_urls)} URLs")

if __name__ == "__main__":
    generate_sitemap()