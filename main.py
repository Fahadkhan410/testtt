#https://github.com/byte-capsule/

import requests
import json
import urllib3
urllib3.disable_warnings()


class Jadoo():
 def __init__(byte_capsule):
  byte_capsule.api_login="https://api.jadoodigital.com/api/v2.1/user/auth/login"
  byte_capsule.api_channels="https://api.jadoodigital.com/api/v2.1/user/channel"
  byte_capsule.api_channel_info="https://api.jadoodigital.com/api/v2.1/user/channel/"
  byte_capsule.headers= {
  'User-Agent': "Mozilla/5.0 (Linux; Android 14; 23021RAAEG Build/UKQ1.230917.001) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.6668.100 Mobile Safari/537.36",
  'Accept': "application/json, text/plain, */*",
  'Accept-Encoding': "gzip",
  'Authorization':None,#"Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE3Mjg5MTIwMzMsIm5iZiI6MTcyODkxMjAzMywianRpIjoiZDVmNTAwMTAtNzAxMi00MmNhLWI5NTgtYTBiOGNhMmUzYmYwIiwiZXhwIjoxNzI4OTEyMzMzLCJpZGVudGl0eSI6eyJpZCI6ImQ0NzcyNDZlOWU3MjRmODFhMDExYjg0NzQ1N2U3MWM0IiwiZG9tYWluIjoiYWYxZGQ4NmMzZmI4NDQ4ZTg3YmI3NzcwMDAwYzkzMGMiLCJwYWNrYWdlIjoiYjg3YTQ0MWYwZjIzNDE1ZmI1MGIwZWNiOGY5NTUyYWQifSwiZnJlc2giOmZhbHNlLCJ0eXBlIjoiYWNjZXNzIn0.rOFRHlMKXJ_zQqpDPp6RLy3J8EVA3mxlH0x4OHEGEZ8",
  'Origin': "https://iptv.jadoodigital.com",
  'Referer': "https://iptv.jadoodigital.com/",}
  byte_capsule.access_token=None
  byte_capsule.refresh_token=None
   
 def login(byte_capsule,user,password,domain):
  req = requests.post(url=byte_capsule.api_login,json={
  "username":user,
  "password":password,
  "domain":domain},headers=byte_capsule.headers,verify=False)
  try:
   req_json=json.loads(req.text)
   if req_json["status"]=="SUCCESS":
    print("[✓] Login Successful ......")
    byte_capsule.access_token=req_json["data"]["access_token"]
    byte_capsule.refresh_token=req_json["data"]["refresh_token"]
    byte_capsule.headers["Authorization"]="Bearer "+byte_capsule.access_token
    return True
   else:
      print("[X] Login Failed !!!!.....")
      return False
    
  except Exception as error:
    print("[X] Sever Error .......",error)
    return False
 def get_channels(byte_capsule):
  req=requests.get(url=byte_capsule.api_channels,headers=byte_capsule.headers,verify=False)
  try:
   req_json=json.loads(req.text)
   if req_json["status"]=="SUCCESS":
      print("[✓] Channel list ......")
      all_data=[]
      count=0
      for channel in req_json["data"]["channels"]:
       data={"name":channel["name"],"slug":channel["slug"],"logo":channel["logo"]}
       all_data.append(data)
          
       count+=1
       print(f"[{count}] {data['name']}")
      return all_data
  except Exception as error:
   print("[X] Server Error ....",error)
 def get_channel_info(byte_capsule,name,slug):
  req = requests.get(byte_capsule.api_channel_info+slug, headers=byte_capsule.headers,verify=False)
  try:
   req_json=json.loads(req.text)
   if req.status_code==200:
      stream_url=req_json["url"]
      print(f"[✓] {name} : {stream_url}")
      return stream_url
   else:
      print(f"[X] Falied to get {name} info !!! ....")
      
  except Exception as error:
   print("[X] Server Error ....",error)
  
       
def universal_playlist_converter(output_file_name,json_data):
    text = "#EXTM3U"
    for channel in json_data:
        
        name = channel["name"]
        link=channel["stream_link"]
        
        logo=channel["logo"]
        category_name ="Byte Capsule"
        text += f"\n#EXTINF:-1 tvg-name=\"{name}\" tvg-logo=\"{logo}\" tvg-id=\"{id}\" group-title=\"{category_name}\",{name}"
        text += f"\n{link}"
    with open(output_file_name,"w") as w:
        w.write(text)
    return text      
    
    
  
  

if __name__=="__main__":
 app=Jadoo()
 if app.login("jadoo3399","jadoo3399","af1dd86c3fb8448e87bb7770000c930c")==True:
  all_channel=app.get_channels()
  for channel in all_channel:
   stream_url=app.get_channel_info(channel["name"],channel["slug"])
   channel["stream_link"]=stream_url
 #Generate Playlist and Save
  universal_playlist_converter("jadoo_playlist.m3u",all_channel)
