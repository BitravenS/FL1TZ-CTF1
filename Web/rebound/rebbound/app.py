from flask import Flask, render_template, request, session, redirect, url_for, send_file
import uuid
import os
import re
import socket
import requests
import base64

app = Flask(__name__)
app.secret_key = os.urandom(64)


users = {
    "test": {
        "password": "69testpass420",
        "uuid": str(uuid.uuid4()),
        "files": []
    },
    "admin": {
        "password": os.urandom(64),
        "uuid": str(uuid.uuid4()),
        "files": []
    }
}
flag = "FL1TZ{Reb1nd1nG_K1Ng_SakuRaG1_HaNAmichi}"

os.makedirs("files", exist_ok=True)
for user in users:
    user_dir = f"files/{users[user]['uuid']}"
    os.makedirs(user_dir, exist_ok=True)
flag_file_path = f"files/{users['admin']['uuid']}/flag.txt"
with open (flag_file_path,'w') as f:
    f.write(f"welcome admin here is your flag :{flag}")
def is_valid_url(url):
    try:
        regex = re.compile(
            r'^(?:http|https)://'
            r'(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|'
            r'(?:%[0-9a-fA-F][0-9a-fA-F]))+$'
        )
        if not re.match(regex, url):
            return False
        hostname = url.split("//")[-1].split("/")[0].split(":")[0]
        ip_address = socket.gethostbyname(hostname)
        if ip_address.startswith(("127.", "192.168.", "10.")):
            return False
        return True
    except Exception:
        return False

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username in users and users[username]["password"] == password:
            session["username"] = username
            return redirect(url_for("dashboard"))
        return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            return render_template("signup.html", error="Username and password are required")

        if username in users:
            return render_template("signup.html", error="Username already exists")

        user_uuid = str(uuid.uuid4())
        users[username] = {
            "password": password,
            "uuid": user_uuid,
            "files": []
        }

        user_dir = f"files/{user_uuid}"
        os.makedirs(user_dir, exist_ok=True)

        return redirect(url_for("login"))

    return render_template("signup.html")

@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect(url_for("login"))
    username = session["username"]
    user_uuid = users[username]["uuid"]
    user_files = os.listdir(f"files/{user_uuid}")
    return render_template("dashboard.html", username=username, user_uuid=user_uuid, files=user_files)

@app.route("/logout")
def logout():
    if "username" in session:
        username = session.pop("username")
        user_uuid = users[username]["uuid"]
        user_dir = f"files/{user_uuid}"
        if os.path.exists(user_dir):
            for file in os.listdir(user_dir):
                os.remove(os.path.join(user_dir, file))
            os.rmdir(user_dir)
    return redirect(url_for("login"))

@app.route("/submit-url", methods=["POST"])
def submit_url():
    if "username" not in session:
        return redirect(url_for("login"))
    url = request.form.get("url")
    if not url:
        return "URL is required", 400
    if not is_valid_url(url):
        return "Invalid or forbidden URL", 403

    username = session["username"]
    user_uuid = users[username]["uuid"]
    file_name = f"html_{uuid.uuid4().hex}.txt"
    file_path = f"files/{user_uuid}/{file_name}"

    try:
        response = requests.get(url, timeout=5)
        encoded_content = base64.b64encode(response.text.encode("utf-8")).decode("utf-8")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(encoded_content)
    except requests.RequestException as e:
        return f"Error fetching URL: {str(e)}", 500

    return redirect(url_for("dashboard"))

@app.route("/files/<user_uuid>/<filename>")
def serve_file(user_uuid, filename):
    user_path = f"files/{user_uuid}"
    file_path = os.path.join(user_path, filename)
    if os.path.exists(file_path):
        return send_file(file_path, mimetype="text/plain")
    return "File not found", 404

@app.route("/users")
def list_users():
    if request.remote_addr != "127.0.0.1":
        return "Forbidden", 403
    return {user: {"uuid": users[user]["uuid"]} for user in ["test", "admin"] if user in users}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1030)
