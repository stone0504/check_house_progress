import requests
import time
from bs4 import BeautifulSoup
import hashlib
import datetime
try:
    from zoneinfo import ZoneInfo
except ImportError:
    from backports.zoneinfo import ZoneInfo

url = "http://www.sccoltd.com.tw/in-progress/123"  #target
check_interval = 7200

def get_table_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table')
    return table.text if table else ""


def get_content_hash(content):
    return hashlib.md5(content.encode()).hexdigest()

def now_time():
    now_utc = datetime.datetime.now(ZoneInfo("UTC"))
    taipei_time = now_utc.astimezone(ZoneInfo("Asia/Taipei"))
    return taipei_time.strftime("%Y-%m-%d %H:%M:%S")

def notify(message):
    line_notify_token = "XXXXX"
    line_notify_api = "https://notify-api.line.me/api/notify" #token
    headers = {"Authorization": f"Bearer {line_notify_token}"}
    payload = {"message": message}
    requests.post(line_notify_api, headers=headers, data=payload)

def notify_group(message):
    line_notify_token = "XXXXX" #token
    line_notify_api = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": f"Bearer {line_notify_token}"}
    payload = {"message": message}
    requests.post(line_notify_api, headers=headers, data=payload)


previous_hash = ""


while True:
    try:
        table_content = get_table_content(url)
        current_hash = get_content_hash(table_content)

        if previous_hash and current_hash != previous_hash:
            print(f"{now_time()}: New updates")
            notify(f"{now_time()}: House has updates!")
            notify_group(f"{now_time()}: House has updates!")
        else:
            print(f"{now_time()}: No updates")

        previous_hash = current_hash
        time.sleep(check_interval)
    except Exception as e:
        print(f"ERROR: {e}")
        time.sleep(check_interval)
        
        


