from flask import Flask, request, redirect

app = Flask(__name__)

@app.route('/')
def index():
    return '''
    <form action="/login" method="post">
        Username: <input name="username"><br>
        Password: <input name="password" type="password"><br>
        <input type="submit" value="Login">
    </form>
    '''

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    # 驗證邏輯，可接資料庫或固定帳密
    if username == "test" and password == "1234":
        # Web Auth 成功 → Redirect 回 Ruckus 提供的成功 URL
        return redirect("http://10.0.0.1/success")
    else:
        return "Login Failed"
