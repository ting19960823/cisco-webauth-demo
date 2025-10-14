from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)

# 登入頁面 HTML
login_page = """
<!DOCTYPE html>
<html>
  <head>
    <title>Guest WiFi Login</title>
  </head>
  <body>
    <h2>Guest WiFi Login</h2>
    <form action="/login" method="post">
      Username: <input type="text" name="username"><br><br>
      Password: <input type="password" name="password"><br><br>
      <input type="hidden" name="login_url" value="{{ login_url }}">
      <input type="submit" value="Login">
    </form>
  </body>
</html>
"""

@app.route("/")
def index():
    login_url = request.args.get("login_url", "")
    return render_template_string(login_page, login_url=login_url)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template_string("""
            <form method="post">
                <label>Username:</label><input name="username"><br>
                <label>Password:</label><input name="password" type="password"><br>
                <button type="submit">Login</button>
            </form>
        """)
    elif request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # 這裡可以加驗證邏輯，例如查資料庫或固定帳密測試
        if username == "test" and password == "1234":
            return "Login success! You can now access the network."
        else:
            return "Invalid credentials."

app.run(host="0.0.0.0", port=8080)
