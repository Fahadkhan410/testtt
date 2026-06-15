import urllib.request
import json

SOURCE_URL = "https://raw.githubusercontent.com/srhady/axsports/refs/heads/main/live_sports.json"
OUTPUT_FILE = "live_sports.m3u"

def main():
    try:
        req = urllib.request.Request(
            SOURCE_URL, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        with urllib.request.urlopen(req) as response:
            raw_data = response.read().decode('utf-8')
        
        data = json.loads(raw_data)
        channels = data.get("live_matches", [])
        
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as m3u:
            m3u.write("#EXTM3U\n\n")
            
            counter = 0
            for item in channels:
                if not isinstance(item, dict):
                    continue
                
                # 1. Grab the channel name
                name = item.get("title") or item.get("slug") or f"Sports Match {counter+1}"
                group = item.get("sport_name", "Sports")
                logo = item.get("logo") or ""
                
                # 2. Look for the stream URL across all possible hidden key names
                url = (
                    item.get("url") or 
                    item.get("link") or 
                    item.get("stream") or 
                    item.get("m3u8") or 
                    item.get("source") or
                    item.get("stream_url")
                )
                
                # 3. Write it out if a URL is found
                if url:
                    metadata = f'#EXTINF:-1 tvg-logo="{logo}" group-title="{group}",{name}'
                    m3u.write(f"{metadata}\n")
                    m3u.write(f"{url}\n\n")
                    counter += 1
                else:
                    # Debug message to see what keys exist inside their match objects
                    if counter == 0 and len(item.keys()) > 0:
                        print(f"Debug: Available fields in match object: {list(item.keys())}")
                        
        print(f"Success! Processed and compiled {counter} live matches into your M3U playlist.")

    except Exception as e:
        print(f"Error during execution: {e}")

if __name__ == "__main__":
    main()
