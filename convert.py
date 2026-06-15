import urllib.request
import json

SOURCE_URL = "https://raw.githubusercontent.com/srhady/axsports/refs/heads/main/live_sports.json"
OUTPUT_FILE = "live_sports.m3u"

def main():
    try:
        # Fetch the JSON data from the source URL
        req = urllib.request.Request(
            SOURCE_URL, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        with urllib.request.urlopen(req) as response:
            raw_data = response.read().decode('utf-8')
        
        data = json.loads(raw_data)
        
        # Target the specific 'live_matches' array from the source JSON structure
        channels = data.get("live_matches", [])
        
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as m3u:
            m3u.write("#EXTM3U\n\n")
            
            counter = 0
            for item in channels:
                if not isinstance(item, dict):
                    continue
                
                # Extract using the source's custom keys
                name = item.get("title", f"Sports Channel {counter+1}")
                url = item.get("url") or item.get("link")
                group = item.get("sport_name", "Sports")
                logo = item.get("logo") or ""
                
                # Only write to the playlist if a stream link exists
                if url:
                    metadata = f'#EXTINF:-1 tvg-logo="{logo}" group-title="{group}",{name}'
                    m3u.write(f"{metadata}\n")
                    m3u.write(f"{url}\n\n")
                    counter += 1
                        
        print(f"Success! Processed and compiled {counter} live matches into your M3U playlist.")

    except Exception as e:
        print(f"Error during execution: {e}")
        # Ensure the file isn't left empty in case of a breakdown
        try:
            with open(OUTPUT_FILE, 'a', encoding='utf-8') as m3u:
                pass
        except:
            pass

if __name__ == "__main__":
    main()
