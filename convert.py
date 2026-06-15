import urllib.request
import json
import sys

SOURCE_URL = "https://raw.githubusercontent.com/srhady/axsports/refs/heads/main/live_sports.json"
OUTPUT_FILE = "live_sports.m3u"

def main():
    try:
        # 1. Fetch JSON data with a realistic User-Agent header
        req = urllib.request.Request(
            SOURCE_URL, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        )
        with urllib.request.urlopen(req) as response:
            raw_data = response.read().decode('utf-8')
            data = json.loads(raw_data)
        
        # 2. Extract the actual list of channels dynamically
        channels = []
        if isinstance(data, list):
            channels = data
        elif isinstance(data, dict):
            # If the JSON is an object, look inside common keys like 'channels', 'streams', or 'live'
            for key in ['channels', 'streams', 'live', 'data', 'matches']:
                if key in data and isinstance(data[key], list):
                    channels = data[key]
                    break
            # Fallback: if no list key is found, check if the dictionary values contain a list
            if not channels:
                for val in data.values():
                    if isinstance(val, list):
                        channels = val
                        break

        if not channels:
            print("Error: Could not locate a valid list of items in the JSON structure.")
            print(f"Sample data structure received: {str(data)[:200]}")
            sys.exit(1)

        # 3. Write data to M3U format
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as m3u:
            m3u.write("#EXTM3U\n\n")
            
            counter = 0
            for item in channels:
                if not isinstance(item, dict):
                    continue
                
                # Check for flexible naming variations inside the JSON fields
                name = item.get("name") or item.get("title") or item.get("channel_name") or f"Channel {counter+1}"
                url = item.get("url") or item.get("link") or item.get("stream")
                logo = item.get("logo") or item.get("logo_url") or item.get("tvg-logo") or ""
                group = item.get("group") or item.get("category") or item.get("group-title") or "Sports"

                if not url:
                    continue

                metadata = f'#EXTINF:-1 tvg-logo="{logo}" group-title="{group}",{name}'
                m3u.write(f"{metadata}\n")
                m3u.write(f"{url}\n\n")
                counter += 1
                
        print(f"M3U Playlist updated successfully. Compiled {counter} channels.")
        
    except Exception as e:
        print(f"Error during conversion execution: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
