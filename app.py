import json
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


# 1. Funktion zum Laden der Beiträge
def load_posts():
    with open("posts.json", "r", encoding="utf-8") as file:
        return json.load(file)


# 2. WICHTIG: Funktion zum Speichern der Beiträge (Muss vor der Route 'add' stehen!)
def save_posts(posts):
    with open("posts.json", "w", encoding="utf-8") as file:
        json.dump(posts, file, indent=2, ensure_ascii=False)


@app.route("/")
def index():
    blog_posts = load_posts()
    return render_template("index.html", posts=blog_posts)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        blog_posts = load_posts()

        # Generiere eine neue eindeutige ID
        new_id = (
            max([post["id"] for post in blog_posts]) + 1 if blog_posts else 1
        )

        # Hole die Daten aus dem HTML-Formular
        new_post = {
            "id": new_id,
            "author": request.form.get("author"),
            "title": request.form.get("title"),
            "content": request.form.get("content"),
        }

        # Hinzufügen und speichern
        blog_posts.append(new_post)
        save_posts(blog_posts)

        return redirect(url_for("index"))

    return render_template("add.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
