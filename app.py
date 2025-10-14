from flask import Flask, request, redirect

app = Flask(__name__)

@app.route('/')
def index():
    # 抓 Ruckus 帶的 StartURL，預設 fallback 為 "/"
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

    if username == "test" and password == "1234":
        # 成功 → redirect 到 Ruckus Captive Portal 指定 URL
        return "Login OK"
    else:
        return "Login Failed"

if __name__ == "__main__":
    app.run(host="192.168.95.100", port=9443)
