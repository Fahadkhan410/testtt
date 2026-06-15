import urllib.request
import json

# The source URL you provided
SOURCE_URL = "https://raw.githubusercontent.com/srhady/axsports/refs/heads/main/live_sports.json"
OUTPUT_FILE = "live_sports.m3u"

def main():
    try:
        # Fetch the JSON data directly from the URL
        req = urllib.request.Request(SOURCE_URL, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
        
        # Open and write the M3U file
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as m3u:
            m3u.write("#EXTM3U\n\n")
            
            for item in data:
                name = item.get("name", "Unknown Channel")
                url = item.get("url")
                logo = item.get("logo", "")
                group = item.get("group", "Sports")

                if not url:
                    continue

                metadata = f'#EXTINF:-1 tvg-logo="{logo}" group-title="{group}",{name}'
                m3u.write(f"{metadata}\n")
                m3u.write(f"{url}\n\n")
                
        print("M3U Playlist updated successfully.")
    except Exception as e:
        print(f"Error during conversion: {e}")

if __name__ == "__main__":
    main()
