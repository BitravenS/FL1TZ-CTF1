from flask import Flask, request, render_template
from string import ascii_lowercase, digits
import redis
import random
import re

app = Flask(__name__)

redis_db = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)

@app.route("/logs", methods=["GET"])
def forbidden():
    return render_template("forbidden.html"), 403


@app.route("/logs/admin_login", methods=["GET"])
def show_admin_logs():
    """Display admin logs."""
    try:
        with open("./logs/admin_logs", "r") as logs_fd:
            logs = logs_fd.read().strip().split("\n")
    except FileNotFoundError:
        logs = []

    return render_template("display-logs.html", logs=logs)


@app.route("/request/authorized_keys", methods=["GET"])
def generate_auth_token():
    """Generate and store an authorization token."""
    auth_token = "".join(random.choices(ascii_lowercase + digits, k=40))

    redis_db.set(auth_token, "1", ex=69)
    return auth_token


@app.route("/request", methods=["GET"])
def forbidden_request():
    """Handle unauthorized requests."""
    return render_template("forbidden.html"), 403


@app.route("/", methods=["GET"])
def admin_dashboard():
    auth_token = request.headers.get("FL1TZ-auth")

    if not auth_token or len(auth_token.strip()) != 40:
        return render_template("forbidden.html"), 403

    auth_token = auth_token.strip()  
    try:
        with open("logs/admin_logs", "r") as logs_fd:
            logs = logs_fd.read().strip()
        expired_tokens = [token.strip() for token in re.findall(r"FL1TZ-auth:([a-z0-9]{40})", logs)]
        if auth_token in expired_tokens:
            return render_template("token-expired.html"), 403
    except FileNotFoundError:
        return render_template("forbidden.html"), 403

    if redis_db.get(auth_token) is None:
        return render_template("forbidden.html"), 403

    with open("logs/admin_logs", "a") as logs_fd:
        logs_fd.write(f"FL1TZ-auth:{auth_token}\n")

    return render_template("admin-dashboard.html")


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)
