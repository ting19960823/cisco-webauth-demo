import os
from flask import Flask, request, render_template_string, redirect, url_for, jsonify
import requests
import json

app = Flask(__name__)

# 必填環境變數（在 Render dashboard 補）
SZ_MANAGEMENT = os.getenv('SZ_MANAGEMENT')  # e.g. "10.0.0.2" or fqdn
SZ_NBI_PORT = os.getenv('SZ_NBI_PORT', '9443')  # default 9443
NBI_USER = os.getenv('NBI_USER', 'admin')   # 任意，controller 接受的 RequestUserName
NBI_PASSWORD = os.getenv('NBI_PASSWORD')    # 這個要跟 controller 上設定的一樣 (RequestPassword)
USE_TLS = os.getenv('USE_TLS', '1') == '1'

NBI_URL = ("https://" if USE_TLS else "http://") + f"{SZ_MANAGEMENT}:{SZ_NBI_PORT}/portalintf"

# 簡單 login form — Ruckus 會 redirect 並帶參數 (uip, client_mac, url, proxy, ...)
LOGIN_HTML = """
<!doctype html>
<title>Hotspot Login</title>
<h3>Hotspot Login</h3>
<form method="post" action="/login">
  <input type="hidden" name="uip" value="{{uip}}">
  <input type="hidden" name="client_mac" value="{{client_mac}}">
  <input type="hidden" name="url" value="{{url}}">
  <input type="hidden" name="proxy" value="{{proxy}}">
  Username: <input name="username"><br>
  Password: <input type="password" name="password"><br>
  <button type="submit">Login</button>
</form>
"""

@app.route('/')
def index():
    # Ruckus redirect 會把參數放到 query string，取出並填入表單 hidden
    uip = request.args.get('uip', '')
    client_mac = request.args.get('client_mac', '')
    url_ = request.args.get('url', '')
    proxy = request.args.get('proxy', '')
    return render_template_string(LOGIN_HTML, uip=uip, client_mac=client_mac, url=url_, proxy=proxy)

def call_nbi(payload):
    headers = {'Content-Type': 'application/json'}
    try:
        r = requests.post(NBI_URL, headers=headers, json=payload, verify=False, timeout=10)
        return r.status_code, r.text
    except Exception as e:
        return None, str(e)

@app.route('/login', methods=['POST'])
def login():
    # 從 form 得到使用者 creds 與 Ruckus 傳來的 uip/client_mac
    username = request.form.get('username')
    password = request.form.get('password')
    uip = request.form.get('uip')       # 通常是 ENC...（已被 Ruckus 加密）
    client_mac = request.form.get('client_mac')
    # Build JSON for LoginAsync (非同步) 或 Login (同步) - 這裡示範 LoginAsync
    payload = {
        "Vendor": "ruckus",
        "RequestUserName": "admin",
        "RequestPassword": "1qazXSW@",
        "APIVersion": "1.0",
        "RequestCategory": "UserOnlineControl",
        "RequestType": "LoginAsync",
        "UE-IP": uip,
        "UE-MAC": client_mac,
        "UE-Proxy": "0",
        "UE-Username": username,
        "UE-Password": password
    }
    code, text = call_nbi(payload)
    # 回傳 controller 回應給 operator（或你可解析 JSON，並根據 ResponseCode 做不同處理）
    return f"NBI POST status: {code}\n\n{text}", 200, {'Content-Type': 'text/plain'}

# 範例: poll status (前端可用 AJAX 定期 call)
@app.route('/status', methods=['POST'])
def status():
    uip = request.form.get('uip')
    client_mac = request.form.get('client_mac')
    payload = {
        "Vendor": "ruckus",
        "RequestUserName": NBI_USER,
        "RequestPassword": NBI_PASSWORD,
        "APIVersion": "1.0",
        "RequestCategory": "UserOnlineControl",
        "RequestType": "Status",
        "UE-IP": uip,
        "UE-MAC": client_mac
    }
    code, text = call_nbi(payload)
    return text, 200, {'Content-Type': 'application/json'}

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
