from flask import Flask, request, render_template_string

app = Flask(__name__)

# 顯示登入頁面
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
