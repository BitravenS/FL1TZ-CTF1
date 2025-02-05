import os
import tarfile
import sqlite3
from flask import Flask, request, render_template, redirect, url_for, session, send_file
from werkzeug.security import generate_password_hash, check_password_hash

UPLOAD_BASE = "/tmp/uploads"
EXTRACT_BASE = "/tmp/extracted"

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Ensure base directories exist
os.makedirs(UPLOAD_BASE, exist_ok=True)
os.makedirs(EXTRACT_BASE, exist_ok=True)

# Initialize database
DB_FILE = "users.db"

def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT UNIQUE NOT NULL,
                            password TEXT NOT NULL)''')
        conn.commit()

init_db()

# Helper function for DB queries
def query_db(query, args=(), one=False):
    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.execute(query, args)
        rv = cur.fetchall()
        conn.commit()
        return (rv[0] if rv else None) if one else rv

# Home page with login check
@app.route("/")
def index():
    if "user" in session:
        return redirect(url_for("dashboard"))
    return render_template("index.html")

# Signup
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        hashed_pw = generate_password_hash(password)

        try:
            query_db("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_pw))
            os.makedirs(os.path.join(UPLOAD_BASE, username), exist_ok=True)
            os.makedirs(os.path.join(EXTRACT_BASE, username), exist_ok=True)
            return redirect(url_for("login"))
        except:
            return "Username already exists!", 400
    return render_template("signup.html")

# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = query_db("SELECT * FROM users WHERE username = ?", (username,), one=True)

        if user and check_password_hash(user[2], password):
            session["user"] = username
            return redirect(url_for("dashboard"))
        return "Invalid credentials", 400
    return render_template("login.html")

# Logout
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("index"))

# User Dashboard
@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))

    username = session["user"]
    user_upload_dir = os.path.join(UPLOAD_BASE, username)
    user_extract_dir = os.path.join(EXTRACT_BASE, username)

    if request.method == "POST":
        if "file" not in request.files:
            return "No file uploaded", 400

        file = request.files["file"]
        if file.filename == "":
            return "No selected file", 400

        file_path = os.path.join(user_upload_dir, "uploads.tar.gz")
        file.save(file_path)

        with tarfile.open(file_path, "r:gz") as tar:
            tar.extractall(path=user_extract_dir)  # VULNERABLE: Symlinks are not removed!

        return "Files extracted! Go to <a href='/files'>/files</a>."

    return render_template("dashboard.html", username=username)

# List files
@app.route("/files")
def list_files():
    if "user" not in session:
        return redirect(url_for("login"))

    username = session["user"]
    user_extract_dir = os.path.join(EXTRACT_BASE, username)
    files = os.listdir(user_extract_dir)
    return render_template("files.html", files=files)

# View file
@app.route("/view/<path:filename>")
def view_file(filename):
    if "user" not in session:
        return redirect(url_for("login"))

    username = session["user"]
    file_path = os.path.join(EXTRACT_BASE, username, filename)
    
    if not os.path.exists(file_path):
        return "File not found", 404

    return send_file(file_path)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
