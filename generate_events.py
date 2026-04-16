#!/usr/bin/env python3
import json
import os
from datetime import datetime, timedelta
import random

categories = [
    ("sports", "Sports", ["F1 Grand Prix", "NBA Finals", "NFL Game", "World Cup", "Tennis Open", "MMA Fight", "Boxing Match", "NASCAR Race", "Marathon", "Golf Major"]),
    ("music", "Music", ["Music Festival", "Concert Tour", "Arena Show", "Festival", "Live Performance", "Band Tour", "Solo Artist", "DJ Set", "Orchestra", "Jazz Festival"]),
    ("gaming", "Gaming", ["Game Launch", "Beta Test", "DLC Release", "Tournament", "Esports Event", "Convention", "Expo", "Gaming Show", "Stream Event", "Game Awards"]),
    ("tech", "Tech", ["Product Launch", "Developer Conference", "Tech Summit", "AI Event", "Hardware Launch", "Software Release", "Update Launch", "Innovation Day", "Tech Expo", "Conference"]),
    ("shopping", "Shopping", ["Sale Event", "Clearance", "Flash Sale", "Launch Sale", "Seasonal Sale", "Holiday Sale", "Anniversary Sale", "Member Sale", "Exclusive Drop", "Launch"]),
    ("entertainment", "Entertainment", ["Movie Premiere", "TV Series Finale", "Show Finale", "Season Premiere", "Special Episode", "Concert Film", "Documentary", "Live Show", "Comedy Special", "Special Event"]),
    ("holiday", "Holiday", ["Holiday", "Festival", "Celebration", " observance", "Observation", "Day", "Event", " Tradition", "Gathering", "Festivity"]),
    ("science", "Science", ["Eclipse", "Launch", "Mission Start", "Discovery", "Research", "Experiment", "Study", "Breakthrough", "Announcement", "Conference"]),
]

locations = [
    "New York", "Los Angeles", "Miami", "Las Vegas", "Tokyo", "London", "Paris", "Berlin", "Sydney", "Toronto",
    "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio", "San Diego", "Dallas", "Austin", "Seattle", "Denver",
    "Boston", "Detroit", "Nashville", "Portland", "Vegas", "Orlando", "Atlanta", "Seattle", "Minneapolis", "New Orleans",
    "Rome", "Madrid", "Barcelona", "Amsterdam", "Munich", "Milan", "Vienna", "Prague", "Dubai", "Singapore",
    "Hong Kong", "Seoul", "Bangkok", "Mumbai", "São Paulo", "Mexico City", "Cairo", "Moscow", "Beijing", "Shanghai"
]

event_templates = [
    "{location} {event_type}",
    "{event_type} {location}",
    "{location} {event_type} {year}",
    "{event_type} at {location}",
    "The {location} {event_type}",
    "{event_type} - {location}",
]

def generate_events(count=10000):
    events = []
    base_date = datetime(2026, 1, 1)
    
    for i in range(count):
        cat_idx = i % len(categories)
        cat_name, cat_display, event_types = categories[cat_idx]
        
        loc = locations[i % len(locations)]
        evt_type = event_types[i % len(event_types)]
        
        event_date = base_date + timedelta(days=random.randint(0, 730))
        date_str = event_date.strftime("%Y-%m-%d")
        
        slug_base = f"{cat_name}-{loc.lower().replace(' ', '-')}-{i}"
        slug = f"event-{i:05d}"
        
        name = f"{loc} {evt_type}"
        
        events.append({
            "name": name,
            "category": cat_name,
            "category_display": cat_display,
            "slug": slug,
            "date": date_str,
            "description": f"{name} - A major {cat_display.lower()} event in {loc}.",
            "location": loc,
            "year": event_date.year
        })
    
    return events

def generate_html(event, template_path, output_dir):
    import re
    
    event_date = datetime.strptime(event["date"], "%Y-%m-%d")
    now = datetime(2026, 4, 16)
    delta = event_date - now
    
    days = max(0, delta.days)
    hours = random.randint(0, 23)
    minutes = random.randint(0, 59)
    seconds = random.randint(0, 59)
    
    meta_description = f"When is the next {event['name']}? The next event is on {event['date']}. Get countdown and schedule."
    title = f"When is the next {event['name']}? | {event['date']}"
    canonical_url = f"https://whenisthenext.com/{event['slug']}/index.html"
    
    with open(template_path, 'r') as f:
        template = f.read()
    
    html = template.replace("{meta_description}", meta_description)
    html = html.replace("{title}", title)
    html = html.replace("{canonical_url}", canonical_url)
    html = html.replace("{question}", f"When is the next {event['name']}?")
    html = html.replace("{answer}", f"The next {event['name']} is on {event['date']}.")
    html = html.replace("{hero_title}", event["name"])
    html = html.replace("{hero_subtitle}", f"Countdown to {event['name']} in {event['location']}")
    html = html.replace("{slug}", event["slug"])
    html = html.replace("{category}", event["category"])
    html = html.replace("{category_display}", event["category_display"])
    html = html.replace("{event_name}", event["name"])
    html = html.replace("{event_answer}", f"The next {event['name']} is scheduled for {event['date']}.")
    html = html.replace("{target_date}", event["date"])
    html = html.replace("{days}", str(days))
    html = html.replace("{hours}", str(hours))
    html = html.replace("{minutes}", str(minutes))
    html = html.replace("{seconds}", str(seconds))
    html = html.replace("{description}", event["description"])
    html = html.replace("{search_query}", event["name"].lower().replace(' ', '+'))
    
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "index.html")
    
    with open(output_path, 'w') as f:
        f.write(html)
    
    return output_path

def main():
    print("Generating 10,000+ events...")
    
    events = generate_events(10000)
    
    print(f"Created {len(events)} events")
    
    with open('events-data.json', 'w') as f:
        json.dump(events, f, indent=2)
    
    print("Saved events to events-data.json")
    
    template_path = 'template.html'
    output_base = 'events'
    
    for i, event in enumerate(events):
        slug_dir = os.path.join(output_base, event['slug'])
        generate_html(event, template_path, slug_dir)
        if (i + 1) % 1000 == 0:
            print(f"Generated {i + 1} pages...")
    
    print(f"Done! Generated {len(events)} event pages in {output_base}/")

if __name__ == "__main__":
    main()