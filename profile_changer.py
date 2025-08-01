import tls_client
import json
import base64
from PIL import Image
from io import BytesIO
import requests
import websocket
import time
import random

GREEN = '\033[92m'
RED = '\033[31m'
END = '\033[0m'

used_tokens = []
used_profiles = []

def onliner(token):
    ws = websocket.WebSocket()

    ws.connect("wss://gateway.discord.gg/?encoding=json&v=9&compress=zlib-stream")
    time.sleep(0.1)
    ws.send(json.dumps({"op": 2,"d": {"token": token,"properties": {"$os": "Windows",},},}))


with open("data.json", "r") as f:
    profiles = json.load(f)

tokens = []
with open("token.txt", "r") as f:
    for line in f:
        token = line.strip()
        if token:
            tokens.append(token)



for token, profile in zip(tokens, profiles):
    status = random.choice(["Wg4KCAoGb25saW5lGgIIAQ==","WgwKBgoEaWRsZRoCCAE=","WgsKBQoDZG5kGgIIAQ=="])
    r=requests.patch("https://discord.com/api/v9/users/@me/settings-proto/1",headers={"authorization":token},json={"settings":status})
    if r.status_code == 200:
        print(f"[{GREEN}ステータス{END}] {token[:30]}")
    else:
        print(f"[{RED}ステータス{END}] {response.text} {token[:30]}")

    onliner(token)
    session = tls_client.Session(client_identifier="chrome_130", random_tls_extension_order=True)
    headers = {
        'accept': '*/*',
        'accept-language': 'ja',
        'authorization': token,
        'content-type': 'application/json',
        'origin': 'https://discord.com',
        'priority': 'u=1, i',
        'referer': 'https://discord.com/channels/@me',
        'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        'x-debug-options': 'bugReporterEnabled',
        'x-discord-locale': 'ja',
        'x-discord-timezone': 'Asia/Tokyo',
        'x-super-properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImphIiwiaGFzX2NsaWVudF9tb2RzIjpmYWxzZSwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEzMC4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTMwLjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjQyNDk2NSwiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbCwiY2xpZW50X2xhdW5jaF9pZCI6ImVlZTExZmZhLTA3NWYtNGExOC1iMTMyLTIwYWNlN2VkMTgxOSIsImxhdW5jaF9zaWduYXR1cmUiOiIxMjY1MjU0Mi04NDgzLTQxYTItOGM2Yy1kNWIzNGNiNmE0ZjQiLCJjbGllbnRfYXBwX3N0YXRlIjoiZm9jdXNlZCIsImNsaWVudF9oZWFydGJlYXRfc2Vzc2lvbl9pZCI6IjE0ZDcyMDEwLWM0NGItNDYwYS04ZWE3LTdlMzhjMTkwNDNjMSJ9',
    }

    global_name = profile["user"].get("global_name", None)
    bio = profile["user"].get("bio", None)
    user_id = profile["user"].get("id", None)
    avatar_uuid = profile["user"].get("avatar", None)
    pronouns = profile["user_profile"].get("pronouns", None)

    json_data = {
        'global_name': global_name if global_name is not None else "Sivaus",
    }

    if avatar_uuid:
        response = requests.get(f"https://cdn.discordapp.com/avatars/{user_id}/{avatar_uuid}.webp")
        if response.status_code == 200:

            img = Image.open(BytesIO(response.content))
            png_buffer = BytesIO()
            img.save(png_buffer, format="PNG")
            avatar_base64 = base64.b64encode(png_buffer.getvalue()).decode('utf-8')
            data_uri = f"data:image/png;base64,{avatar_base64}"
            json_data['avatar'] = data_uri
        else:
            print(f"画像取得に失敗しました。")
            continue

    response = session.patch('https://discord.com/api/v9/users/@me', headers=headers, json=json_data)
    
    if response.status_code != 200:
        print(f"[{RED}アバター{END}] {response.text} {token[:30]}")

        continue
    print(f"[{GREEN}アバター{END}] {token[:30]}")

    json_data = {}
    if bio is not None:
        json_data['bio'] = bio
    if pronouns is not None:
        json_data['pronouns'] = pronouns

    if json_data:
        response = session.patch('https://discord.com/api/v9/users/@me/profile', headers=headers, json=json_data)
        used_tokens.append(token)
        used_profiles.append(profile)
        if response.status_code != 200:
            print(f"[{RED}プロフィール{END}] {token[:30]}")
        else:
            print(f"[{GREEN}プロフィール{END}] {token[:30]}")

    remaining_tokens = [t for t in tokens if t not in used_tokens]
    with open("token.txt", "w") as f:
        for token in remaining_tokens:
            f.write(token + "\n")

    remaining_profiles = [p for p in profiles if p not in used_profiles]
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(remaining_profiles, f, ensure_ascii=False, indent=2)

input("おわり")
