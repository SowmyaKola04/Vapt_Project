import requests
import json

FireWall_IP = "172.31.1.227"
Token = "h5QxNfGHzkghNbnGfg0qyQbQNfwQqy"
url =   f"http://{FireWall_IP}/api/v2/monitor/system/interface"

HEADERS = {
    "Authorization": f"Bearer {Token}"
}
response = requests.get(url, headers=HEADERS, verify= False)

if response.status_code == 200:
    data = response.json()
    print(jsons.dumps(data, indent=4))
else:
    print(f"[!] Failed: HTTP {response.status_code}")
    print(response.text)
