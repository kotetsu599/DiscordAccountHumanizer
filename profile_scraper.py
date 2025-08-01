import threading
import websocket
import json
import re
import requests
import time
import os
os.system("cls")

GREEN = '\033[92m'
YELLOW = "\033[33m"
RED = '\033[31m'
END = '\033[0m'

TOKEN = ""
guild_id = None
member_ids = []
massping = ""
joined_tokens = [] 
user_ids_fetched = threading.Event()

def on_message(ws, message):
    global member_ids
    message = json.loads(message)
    if message["t"] == "GUILD_MEMBER_LIST_UPDATE":
        for i, member_info in enumerate(message["d"]["ops"][2]["items"]):
            try:
                member_info = message["d"]["ops"][2]["items"][i]
                id = member_info["member"]["user"]["id"]
                member_ids.append(id)
            except:
                pass
        user_ids_fetched.set()
    
def on_open(ws):
    auth_payload = {
        "op": 2,
        "d": {
            "token": TOKEN,
            "properties": {
                "$os": "Windows",
            },
        },
    }
    ws.send(json.dumps(auth_payload))
    time.sleep(1)

    payload = {"op": 37, "d": {"subscriptions": {guild_id: {"typing": True, "activities": True, "threads": True, "channels": {channel_id: [[0, 255]]}}}}}
    ws.send(json.dumps(payload))

def get_user_ids(guild, channel):
    global guild_id, channel_id, user_ids_fetched
    guild_id = guild
    channel_id = channel

    user_ids_fetched.clear()

    ws = websocket.WebSocketApp(
        "wss://gateway.discord.gg/",
        on_message=on_message,
        on_open=on_open
    )

    ws_thread = threading.Thread(target=ws.run_forever)
    ws_thread.start()

    user_ids_fetched.wait()
    return member_ids


channel_link = input("チャンネルリンク:")
pattern = r"https://discord.com/channels/(\d+)/(\d+)"

match = re.match(pattern, channel_link)
if match:
    guild_id = match.group(1)
    channel_id = match.group(2)

user_ids=get_user_ids(guild_id,channel_id)
if user_ids == []:
    print(f"[{RED}メンバー取得{END}]")
    input()
print(f"[{GREEN}メンバー取得{END}] {len(user_ids)}人")

profiles = []
for user_id in user_ids:
    r=requests.get(f"https://discord.com/api/v9/users/{user_id}/profile?type=popout&with_mutual_guilds=true&with_mutual_friends=true&with_mutual_friends_count=false&guild_id={guild_id}",headers={"authorization":TOKEN})
    if r.status_code == 200:
        print(f"[{GREEN}プロフィール取得{END}]")
    elif r.status_code == 429:
        print(f"[{YELLOW}プロフィール取得{END}]")
        time.sleep(3)
        r=requests.get(f"https://discord.com/api/v9/users/{user_id}/profile?type=popout&with_mutual_guilds=true&with_mutual_friends=true&with_mutual_friends_count=false&guild_id={guild_id}",headers={"authorization":TOKEN})
    else:
        print(f"[{RED}プロフィール取得{END}]")
        continue
    if r.json()["user"].get("bot",False):
        continue
    profiles.append(r.json())

with open("data.json", "w") as f:
    json.dump(profiles, f, indent=2)
input("おわり")

    


