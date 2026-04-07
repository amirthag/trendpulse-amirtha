import requests
import json
import time
import os
from datetime import datetime

# API URLs
top_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
item_url = "https://hacker-news.firebaseio.com/v0/item/{}.json"

headers = {"User-Agent": "TrendPulse/1.0"}

# categories with keywords
categories = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"]
}

# function to find category from title
def find_category(title):
    title = title.lower()
    for cat in categories:
        for word in categories[cat]:
            if word in title:
                return cat
    return None


print("Getting top stories...")

# fetch top story IDs
try:
    res = requests.get(top_url, headers=headers)
    top_ids = res.json()[:500]
except:
    print("Error fetching top stories")
    exit()

all_data = []

# track count for each category
count = {cat: 0 for cat in categories}

# loop category-wise
for cat in categories:
    print("Collecting", cat, "stories..")

    for i in top_ids:
        if count[cat] >= 25:
            break

        try:
            r = requests.get(item_url.format(i), headers=headers, timeout=5)
            story = r.json()
        except:
            print("Skipped id", i)
            continue

        if not story:
            continue

        title = story.get("title")
        if not title:
            continue

        found = find_category(title)

        # only take stories matching current category
        if found == cat:
            data = {
                "post_id": story.get("id"),
                "title": title,
                "category": found,
                "score": story.get("score", 0),
                "num_comments": story.get("descendants", 0),
                "author": story.get("by"),
                "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            all_data.append(data)
            count[cat] += 1

    # sleep after each category
    time.sleep(2)


# create data folder if not exists
if not os.path.exists("data"):
    os.makedirs("data")

# create file name with date
file_name = "data/trends_" + datetime.now().strftime("%Y%m%d") + ".json"

# save JSON file
with open(file_name, "w", encoding="utf-8") as f:
    json.dump(all_data, f, indent=4)

print("\nCollected", len(all_data), "stories.")
print("Saved to", file_name)