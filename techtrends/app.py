# coding=utf8

import sqlite3

from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort
from datetime import datetime
import logging

logging.basicConfig(level=logging.DEBUG)

# Function to get a database connection.
# This function connects to database with the name `database.db`
def get_db_connection():
    connection = sqlite3.connect("database.db")
    connection.row_factory = sqlite3.Row
    return connection

# Function to get a post using its ID
def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute("SELECT * FROM posts WHERE id = ?",
                        (post_id,)).fetchone()
    connection.close()
    app.logger.info("Article "+post["Title"]+" Retrieved")
    return post

# Define the Flask application
app = Flask(__name__)
app.config["SECRET_KEY"] = "your secret key"

@app.route("/status")
def health():
    response = app.response_class(
        response=json.dumps({"result":"OK - healthy"}),
        status=200,
        mimetype="application/json"
    )
    
    app.logger.info("Status")
    
    return response

@app.route("/metrics")
def metrics():
    connection = get_db_connection()
    result = connection.execute("SELECT count(*) as count FROM posts").fetchone()
    connection.close()
    response = app.response_class(
        response=json.dumps({"db_connection_count":1,"post_count":result["count"]}),
        status=200,
        mimetype="application/json"
    )
    
    app.logger.info("Metrics")
    
    return response

# Define the main route of the web application 
@app.route("/")
def index():
    connection = get_db_connection()
    posts = connection.execute("SELECT * FROM posts").fetchall()
    connection.close()
    app.logger.info("Index Page")
    return render_template("index.html", posts=posts)

# Define how each individual article is rendered 
# If the post ID is not found a 404 page is shown
@app.route("/<int:post_id>")
def post(post_id):
    post = get_post(post_id)

    if post is None:
      app.logger.info("Post not Found 404")
      return render_template("404.html"), 404
    else:
      return render_template("post.html", post=post)

# Define the About Us page
@app.route("/about")
def about():
    app.logger.info("About Us Page")
    return render_template("about.html")

# Define the post creation functionality 
@app.route("/create", methods=("GET", "POST"))
def create():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]

        if not title:
            flash("Title is required!")
        else:
            connection = get_db_connection()
            connection.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
                         (title, content))
            connection.commit()
            connection.close()
            app.logger.info("Article "+title+" Created")

            return redirect(url_for("index"))

    return render_template("create.html")

# start the application on port 3111
if __name__ == "__main__":
   app.run(host="0.0.0.0", port="3111")
