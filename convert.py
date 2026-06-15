import urllib.request
import json
import sys

SOURCE_URL = "https://raw.githubusercontent.com/srhady/axsports/refs/heads/main/live_sports.json"
OUTPUT_FILE = "live_sports.m3u"

def main():
    print("--- START DIAGNOSTIC TEST ---")
    try:
        # Fetch the raw text from the source URL
        req = urllib.request.Request(
            SOURCE_URL, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        with urllib.request.urlopen(req) as response:
            raw_data = response.read().decode('utf-8')
        
        print("1. Successfully connected to source URL.")
        print(f"2. Raw text length received: {len(raw_data)} characters.")
        
        # Print the first 500 characters of the file into your logs
        print("3. Sneak peek of the first 500 characters:")
        print("=========================================")
        print(raw_data[:500])
        print("=========================================")

        # Parse JSON
        data = json.loads(raw_data)
        print("4. JSON parsed successfully.")
        
        if isinstance(data, list):
            print(f"5. JSON is a LIST containing {len(data)} items.")
            if len(data) > 0:
                print(f"Sample first item keys: {list(data[0].keys()) if isinstance(data[0], dict) else type(data[0])}")
        elif isinstance(data, dict):
            print(f"5. JSON is a DICTIONARY with root keys: {list(data.keys())}")
        else:
            print(f"5. JSON is a strange type: {type(data)}")

        # Keep your previous fallback loop active to try and write what it can
        channels = data if isinstance(data, list) else []
        if isinstance(data, dict):
            for key in ['channels', 'streams', 'live', 'data', 'matches']:
                if key in data and isinstance(data[key], list):
                    channels = data[key]
                    break
        
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as m3u:
            m3u.write("#EXTM3U\n\n")
            counter = 0
            for item in channels:
                if isinstance(item, dict):
                    name = item.get("name") or item.get("title") or f"Channel {counter+1}"
                    url = item.get("url") or item.get("link")
                    if url:
                        m3u.write(f'#EXTINF:-1 group-title="Sports",{name}\n{url}\n\n')
                        counter += 1
                        
        print(f"--- END TEST: Written {counter} channels ---")
        if counter == 0:
            sys.exit("Forcing failure because 0 channels were generated. Check logs above!")

    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
