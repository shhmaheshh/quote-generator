from flask import Flask, render_template, jsonify
import requests
import sqlite3
def init_db():

    conn = sqlite3.connect("quotes.db")

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quotes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            quote TEXT,
            author TEXT
        )
    """)

    conn.commit()
    conn.close()

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/quote")
def get_quote():

    response = requests.get(
        "https://zenquotes.io/api/random"
    )

    data = response.json()

    quote = data[0]["q"]
    author = data[0]["a"]

    conn = sqlite3.connect("quotes.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO quotes (quote, author) VALUES (?, ?)",
        (quote, author)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "quote": quote,
        "author": author
    })
@app.route("/history")
def history():

    conn = sqlite3.connect("quotes.db")

    cursor = conn.cursor()

    cursor.execute("""
        SELECT quote, author
        FROM quotes
        ORDER BY id DESC
        LIMIT 10
    """)

    rows = cursor.fetchall()

    conn.close()

    return jsonify(rows)
init_db()

if __name__ == "__main__":
    app.run(debug=True)