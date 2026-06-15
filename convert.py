import urllib.request
import json

SOURCE_URL = "https://raw.githubusercontent.com/srhady/axsports/refs/heads/main/live_sports.json"
OUTPUT_FILE = "live_sports.m3u"

def main():
    # Force create a fallback file right away so it always exists
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as m3u:
        m3u.write("#EXTM3U\n\n")
        m3u.write('#EXTINF:-1 group-title="System",Playlist Initialized\n')
        m3u.write('http://example.com/init.mp4\n\n')

    try:
        req = urllib.request.Request(SOURCE_URL, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
        
        matches = data.get("live_matches", []) + data.get("upcoming_matches", [])
        
        if matches:
            # Overwrite with real data if matches exist
            with open(OUTPUT_FILE, 'w', encoding='utf-8') as m3u:
                m3u.write("#EXTM3U\n\n")
                for match in matches:
                    if not isinstance(match, dict): continue
                    title = match.get("title", "Match")
                    group = match.get("sport_name", "Sports")
                    
                    for stream in match.get("streams", []):
                        if not isinstance(stream, dict): continue
                        url = stream.get("play_url")
                        server = stream.get("server_name", "")
                        if url:
                            name = f"{title} [Server {server}]" if server else title
                            m3u.write(f'#EXTINF:-1 group-title="{group}",{name}\n{url}\n\n')
            print("Playlist overwritten with fresh match streams.")
    except Exception as e:
        print(f"Source fetch failed, keeping basic initialized file: {e}")

if __name__ == "__main__":
    main()
