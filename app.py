from flask import Flask, request, redirect

app = Flask(__name__)

@app.route('/')
def index():
    start_url = request.args.get('StartURL', '/')
    return f'''
    <form action="/login?StartURL={start_url}" method="post">
        Username: <input name="username"><br>
        Password: <input name="password" type="password"><br>
        <input type="submit" value="Login">
    </form>
    '''

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    start_url = request.args.get('StartURL', '/')
    client_mac = request.args.get('client_mac')
    wlan_id = request.args.get('wlan')
    sz_ip = request.args.get('nbiIP')

    if username == "test" and password == "1234":
        # 通知 SZ144 認證成功
        if sz_ip and client_mac and wlan_id:
            try:
                requests.get(f"http://192.168.95.100:9080/portalintf",
                             params={"mac": client_mac, "username": username, "wlan": wlan_id}, timeout=5)
            except Exception as e:
                print("Error notifying SZ144:", e)

        # Redirect 使用者到原本想去的網址
        return redirect(start_url)
    else:
        return "Login Failed"
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
