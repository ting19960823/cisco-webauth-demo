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

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    login_url = request.form.get("login_url")

    # 模擬帳密驗證（可改成查資料庫或 API）
    if username == "guest" and password == "1234":
        # 登入成功 → Redirect 回 WLC login URL
        return redirect(f"{login_url}?username={username}&password={password}")
    else:
        return "Login failed. Please try again."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
