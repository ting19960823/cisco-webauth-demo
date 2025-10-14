from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)

login_page = """
<h2>Guest WiFi Login</h2>
<form action="/login" method="post">
  <input type="hidden" name="start_url" value="{{ start_url }}">
  Username: <input type="text" name="username"><br>
  Password: <input type="password" name="password"><br>
  <input type="submit" value="Login">
</form>
"""

@app.route("/", methods=["GET"])
def index():
    # 從 SZ redirect 參數抓 StartURL
    start_url = request.args.get("StartURL", "https://google.com")
    return render_template_string(login_page, start_url=start_url)

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    start_url = request.form.get("start_url", "https://google.com")

    # 驗證帳號密碼
    if username == "test" and password == "1234":
        # ✅ 登入成功 → redirect SZ StartURL → client 被放行
        return redirect(start_url)
    else:
        return "Invalid credentials.", 401

app.run(host="0.0.0.0", port=8080)
