import urllib.request
import json

SOURCE_URL = "https://raw.githubusercontent.com/srhady/axsports/refs/heads/main/live_sports.json"
OUTPUT_FILE = "live_sports.m3u"

def main():
    # Base fallback initialization
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as m3u:
        m3u.write("#EXTM3U\n\n")

    try:
        req = urllib.request.Request(SOURCE_URL, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
        
        matches = data.get("live_matches", []) + data.get("upcoming_matches", [])
        
        if matches:
            with open(OUTPUT_FILE, 'w', encoding='utf-8') as m3u:
                m3u.write("#EXTM3U\n\n")
                
                for match in matches:
                    if not isinstance(match, dict): 
                        continue
                    title = match.get("title", "Match")
                    group = match.get("sport_name", "Sports")
                    
                    for stream in match.get("streams", []):
                        if not isinstance(stream, dict): 
                            continue
                        url = stream.get("play_url")
                        server = stream.get("server_name", "")
                        referer = stream.get("required_referer", "https://iframe.rumsport10.live/")
                        
                        if url:
                            name = f"{title} [Server {server}]" if server else title
                            
                            # Append custom Referer and User-Agent headers to bypass security
                            # This tells ZalTV to spoof the required web host
                            protected_url = f"{url}|Referer={referer}&User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                            
                            m3u.write(f'#EXTINF:-1 group-title="{group}",{name}\n{protected_url}\n\n')
            print("Playlist generated successfully with security bypass strings added.")
    except Exception as e:
        print(f"Execution failed: {e}")

if __name__ == "__main__":
    main()
