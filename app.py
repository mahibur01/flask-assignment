from flask import Flask, redirect, url_for, render_template, request, session
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import requests

app = Flask(__name__)
auth = HTTPBasicAuth()


app.secret_key = b'appsecretkey'


# Basic Authentication User
users = {"admin": generate_password_hash("admin")}


# Static Login user
user = {"username": "admin", "password": "admin"}


# Basic Auth verify
@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username


# Base URL
@app.route("/")
@auth.login_required
def index():
    return redirect(url_for("login"))


# login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == user["username"] and password == user["password"]:
            session["user"] = username
            return redirect(url_for("dashboard"))

    return render_template("login.html")


# Dashboard
@app.route("/users/dashboard")
def dashboard():

    # POSTS API
    json_uri = requests.get("https://dummyjson.com/products?limit=10")
    posts = (json_uri.json())["products"]
    if "user" in session and session["user"] == user["username"]:

        return render_template("dashboard.html", user=user, posts=posts)
    else:
        return redirect(url_for("login"))


# Post
@app.route("/users/dashboard/post/<id>")
def post(id):
    json_uri = requests.get("https://dummyjson.com/products?limit=10")
    posts = (json_uri.json())["products"]
    return render_template("post.html", post=posts)


# Logout
@app.route("/users/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

# 404 Page
@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")


if __name__ == "__main__":
    app.run(debug=True)
